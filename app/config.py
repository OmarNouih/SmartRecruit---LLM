import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'TESTINGCHEATS123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    UPLOAD_FOLDER_CV = os.path.join('app', 'static', 'uploads', 'cv')
    UPLOAD_FOLDER_PHOTOS = os.path.join('app', 'static', 'uploads', 'photos')
    API_TOKEN = os.environ.get('API_TOKEN', 'default_api_token')
    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    MONGO_URI = 'mongodb://localhost:27017/applications'
