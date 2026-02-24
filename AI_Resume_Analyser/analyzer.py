from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import re
from jobs_data import jobs

# Load embedding model (AI understanding model)
from sentence_transformers import SentenceTransformer
import streamlit as st

@st.cache_resource
def load_model():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


# -------- Extract text from PDF ----------
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    return text.lower()


# -------- Clean text ----------
def clean_text(text):
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    return text


# -------- Analyze Resume ----------
def analyze_resume(pdf_file):

    model = load_model()

    resume_text = extract_text_from_pdf(pdf_file)
    resume_text = clean_text(resume_text)

    resume_embedding = model.encode(resume_text)

    job_scores = {}
    skill_gap = {}

    for role, skills in jobs.items():

        job_text = " ".join(skills)
        job_embedding = model.encode(job_text)

        similarity = cosine_similarity(
            [resume_embedding],
            [job_embedding]
        )[0][0]

        job_scores[role] = similarity

        # Skill gap detection
        missing = [skill for skill in skills if skill not in resume_text]
        skill_gap[role] = missing

    # Best role
    best_role = max(job_scores, key=job_scores.get)

    return best_role, job_scores, skill_gap[best_role]