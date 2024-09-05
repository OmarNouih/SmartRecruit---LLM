# **RucRut - Intelligent Recruitment Optimization System**

## **Overview**
RucRut is an advanced AI-powered recruitment system designed to enhance and streamline the hiring process for both **job providers** and **candidates**. The platform leverages cutting-edge **Natural Language Processing (NLP)** and **AI models** to generate tailored interview questions based on the candidate’s CV and job requirements, automatically evaluate their responses, and provide comprehensive feedback.

This system is built using **Flask**, **SQLAlchemy**, **MongoDB**, and **Hugging Face's NLP models**, with a focus on offering efficient, bias-reducing, and personalized recruitment experiences.

---

## **Video Walkthrough**

[Click here to watch the video walkthrough](https://drive.google.com/file/d/103M12Ok-hC81KZHVV7FvGC586wEa_KKX/view?usp=sharing)

> *(This video explains how the application works)*

---

## **Features**

### **For Job Providers**
- **Dashboard**: Manage job postings and track candidate applications in real-time.
- **Job Posting Creation**: Create and modify job postings with detailed specifications.
- **AI-Generated Interview Questions**: Automatically generate interview questions based on candidate CV and job description.
- **Automatic Feedback and Scoring**: Receive AI-driven feedback and score candidates based on their interview responses.
- **Analytics and Reports**: View candidate performance metrics through various graphs, such as age distribution, score comparisons, and top performers.

### **For Candidates**
- **Job Search and Application**: Browse and apply for job postings in just a few clicks.
- **AI-Powered Interviews**: Experience tailored interview questions based on your CV and the specific job requirements.
- **Immediate Feedback**: Get real-time feedback on interview responses to improve performance.

---

## **Setup and Installation**

To set up the RucRut application locally, follow these steps:

### **Requirements**
- **Python 3.11+**
- **Flask 2.2.3**
- **MongoDB 4.7.0**
- **SQLAlchemy 2.0.8**

### **Steps**
1. **Clone the repository**:
   ```bash
   git clone https://github.com/OmarNouih/SmartRecruit_LLM.git
   cd RucRut
   ```

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Ensure to configure your `.env` file with the necessary environment variables for the Flask application, MongoDB connection, and Hugging Face API credentials.

4. **Initialize the database**:
   - Set up your SQLite database:
     ```bash
     flask db upgrade
     ```

5. **Run the Flask application**:
   ```bash
   flask run
   ```
   The application will be available on `http://localhost:5000`.

6. **Access MongoDB**:
   - Ensure MongoDB is running, and it's properly configured in the `.env` file.

---

## **How to Use the Application**

### **Job Providers**
1. **Sign up and Log in**.
2. **Create Job Postings**: Add jobs with specific titles, locations, descriptions, and other necessary information.
3. **Manage Applications**: Review candidates’ CVs, interview responses, and scores.
4. **Track Data**: Use the dashboard to view visual insights such as the top 3 candidates, score comparisons, and other analytics.

### **Candidates**
1. **Browse Jobs**: Search and apply for jobs that match your skills.
2. **AI Interview**: Participate in personalized interviews generated based on your CV.
3. **Get Feedback**: Receive instant feedback and improve based on AI evaluations.

---

## **Technologies Used**

- **Backend**: Flask, SQLAlchemy, MongoDB
- **Frontend**: HTML5, CSS3, JavaScript
- **AI Models**: Hugging Face Transformers, Sentence Transformers
- **PDF Parsing**: PDFPlumber

---

## **Contributing**

We welcome contributions to improve the functionality of RucRut. If you'd like to contribute, please:

1. Fork the repository.
2. Create a new branch for your feature/bug fix.
3. Submit a pull request.

---

## **License**

This project is licensed under the **3DSF License**.

---

## **Contact**

For any inquiries, you can reach out to the developers:

- **Omar NOUIH** - [Email](omarnouih@gmail.com)
- **Salma SAHL** - [Email](sahlsalma56@gmail.com)
