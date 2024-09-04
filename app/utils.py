import os
from werkzeug.utils import secure_filename
from flask import current_app
import re
import requests
import json
import time
import logging
import pdfplumber  # type: ignore
from sentence_transformers import SentenceTransformer, util  # type: ignore

# Initialize the sentence transformer model
model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')
logging.basicConfig(level=logging.DEBUG)

def create_upload_folders(app):
    """
    Creates the necessary upload folders for CVs and profile photos.
    If the folders already exist, it does nothing.

    Args:
        app (Flask): The Flask application instance.
    """
    os.makedirs(app.config['UPLOAD_FOLDER_CV'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER_PHOTOS'], exist_ok=True)

def allowed_file(filename, allowed_extensions):
    """
    Checks if a given filename has an allowed extension.

    Args:
        filename (str): The name of the file to check.
        allowed_extensions (set): A set of allowed file extensions.

    Returns:
        bool: True if the file has an allowed extension, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def preprocess_text(text):
    """
    Preprocesses the input text by removing unwanted characters and normalizing spaces.

    Args:
        text (str): The text to preprocess.

    Returns:
        str: The cleaned and normalized text.
    """
    text = re.sub(r'\s+', ' ', text)  
    text = re.sub(r'[^\w\s]', '', text)  
    return text

def compute_similarity(cv_text, job_description):
    """
    Computes the cosine similarity between the CV text and job description.

    Args:
        cv_text (str): The text from the candidate's CV.
        job_description (str): The text from the job description.

    Returns:
        float: The cosine similarity score between the CV and job description.
    """
    cv_text = preprocess_text(cv_text)
    job_description = preprocess_text(job_description)

    embeddings_cv = model.encode(cv_text, convert_to_tensor=True)
    embeddings_job_desc = model.encode(job_description, convert_to_tensor=True)

    similarity_score = util.cos_sim(embeddings_cv, embeddings_job_desc)

    return similarity_score.item()

def evaluate_cv(cv_text, job_description, threshold = 0.5):
    """
    Evaluates the CV against the job description using the similarity score.

    Args:
        cv_text (str): The text from the candidate's CV.
        job_description (str): The text from the job description.
        threshold (float): The similarity threshold to determine a match.

    Returns:
        bool: True if the similarity score is above the threshold, False otherwise.
    """
    similarity = compute_similarity(cv_text, job_description)
    logging.info(f"Similarity score: {similarity:.2f}")

    return similarity > threshold, similarity

def generate_interview_questions(cv_text, job_description, max_retries=10):
    """
    Generates personalized interview questions based on the candidate's CV and the job description.

    Args:
        cv_text (str): The text from the candidate's CV.
        job_description (str): The text from the job description.
        max_retries (int): The maximum number of retries if the API call fails.

    Returns:
        list: A list of generated interview questions or an error message.
    """
    prompt = f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
Generate 10 personalized interview questions based on the candidate's experience and the job description provided. Don't add anything else, just give the 10 questions and don't repeat questions.

### Input:
Candidate's Resume:
{cv_text}

Job Description:
{job_description}

### Response:
"""
    data = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 1000,
            "temperature": 0.6,
            "top_p": 0.9,
            "do_sample": True
        }
    }

    headers = {
        "Authorization": f"Bearer {current_app.config['API_TOKEN']}",
        "Content-Type": "application/json"
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(current_app.config['API_URL'], headers=headers, data=json.dumps(data))
            response.raise_for_status()
            result = response.json()
            logging.debug("API Response: %s", result)

            # Extract questions from the generated text
            generated_text = result[0].get('generated_text', '')
            questions = [line.strip() for line in generated_text.split("\n") if line.strip().endswith('?')]
            logging.debug("Generated Questions: %s", questions)

            # Ensure exactly 10 questions are returned
            if len(questions) == 10:
                return questions
            else:
                logging.warning("Generated questions count is not 10. Attempt %d.", attempt + 1)

        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            # Exponential backoff for retries
            wait_time = (2 ** attempt) + (0.1 * attempt)
            logging.warning(f"Attempt {attempt + 1} failed. Retrying in {wait_time:.2f} seconds... Error: {e}")
            time.sleep(wait_time)
        except Exception as e:
            logging.error(f"Unexpected error occurred: {e}")
            break

    return ["Error: Could not generate questions after multiple attempts."]

def generate_feedback(question_text, response_text, job_description, max_retries=10):
    """
    Generates feedback based on the candidate's response to an interview question, the question itself, and the job description, and generates a score out of 10 at the end.

    Args:
        question_text (str): The interview question asked to the candidate.
        response_text (str): The candidate's response to the interview question.
        job_description (str): The text from the job description.
        max_retries (int): The maximum number of retries if the API call fails.

    Returns:
        str: The generated feedback or an error message.
    """
    prompt = f"""Below is an interview question, the candidate's response, and the job description. Provide concise , short and constructive feedback on the candidate's response, considering the job requirements and the context of the question. Make sure to include a score out of 10 at the end of the feedback. The score should always be formatted as 'Score: X/10'.

    ### Example:
    Feedback: The candidate provided a well-thought-out response, addressing the key requirements of the job description effectively. However, they could improve on their technical knowledge. Score: 7/10

    ### Interview Question:
    {question_text}

    ### Candidate's Response:
    {response_text}

    ### Job Description:
    {job_description}

    ### Feedback:
    """

    data = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.6,
            "top_p": 0.9,
            "do_sample": True
        }
    }

    headers = {
        "Authorization": f"Bearer {current_app.config['API_TOKEN']}",
        "Content-Type": "application/json"
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(current_app.config['API_URL'], headers=headers, data=json.dumps(data))
            response.raise_for_status()
            result = response.json()
            logging.debug("API Feedback Response: %s", result)

            # Extract feedback from the generated text
            generated_text = result[0].get('generated_text', '')
            feedback_start = generated_text.find("### Feedback:") + len("### Feedback:")
            feedback = generated_text[feedback_start:].strip()
            logging.debug("Extracted Feedback: %s", feedback)

            return feedback

        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            # Exponential backoff for retries
            wait_time = (2 ** attempt) + (0.1 * attempt)
            logging.warning(f"Attempt {attempt + 1} failed. Retrying in {wait_time:.2f} seconds... Error: {e}")
            time.sleep(wait_time)
        except Exception as e:
            logging.error(f"Unexpected error occurred: {e}")
            break

    return "Error: Could not generate feedback after multiple attempts."

def convert_keys_to_strings(data):
    """
    Recursively converts all dictionary keys to strings.

    Args:
        data (dict or list): The input dictionary or list to process.

    Returns:
        dict or list: The processed data with all keys converted to strings.
    """
    if isinstance(data, dict):
        return {str(k): convert_keys_to_strings(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_keys_to_strings(i) for i in data]
    else:
        return data

def extract_score(feedback):
    """
    Extracts the score from the feedback text using multiple patterns.

    Args:
        feedback (str): The feedback text containing the score.

    Returns:
        int: The extracted score or None if no score was found.
    """
    patterns = [
        r'\b(\d{1,2})\s*/\s*10\b',                # Matches "3/10", "3 / 10", etc.
        r'\b(\d{1,2})\s*out\s+of\s+10\b',         # Matches "3 out of 10", etc.
        r'\b(\d{1,2})\s*over\s*10\b',             # Matches "3 over 10", etc.
        r'\bscore\s+is\s+(\d{1,2})\b',            # Matches "score is 10", "score is 3", etc.
        r'\brated\s+(\d{1,2})\s*/\s*10\b',        # Matches "rated 7/10", etc.
        r'\brating\s+of\s+(\d{1,2})\s*/\s*10\b',  # Matches "rating of 8/10", etc.
        r'\bgave\s+it\s+a\s+(\d{1,2})\b',         # Matches "gave it a 5", etc.
        r'\b(\d{1,2})\b\s+(?:points|stars)\s*/\s*10\b' # Matches "5 points / 10", "5 stars / 10", etc.
    ]

    for pattern in patterns:
        match = re.search(pattern, feedback, re.IGNORECASE)
        if match:
            return int(match.group(1))

    logging.warning("No score found in feedback.")
    return None
