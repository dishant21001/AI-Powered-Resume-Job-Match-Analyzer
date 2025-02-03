import streamlit as st
import os
import base64
from utils.text_processing import extract_text_from_pdf
from utils.skills_extractor import extract_skills

# --------------------- LOAD CUSTOM STYLES ---------------------
def load_css():
    css_file_path = "assets/styles.css"
    if os.path.exists(css_file_path):
        with open(css_file_path, "r") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# --------------------- DISPLAY LOGO (Centered) ---------------------
def display_logo():
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            encoded_logo = base64.b64encode(image_file.read()).decode()
        
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center; padding-bottom: 10px;">
                <img src="data:image/png;base64,{encoded_logo}" width="250">
            </div>
            """,
            unsafe_allow_html=True
        )

# --------------------- CONFIGURATION ---------------------
# Define High Impact Skills List (Modify based on industry)
HIGH_IMPACT_SKILLS = {
    "python", "sql", "machine learning", "data visualization", "tableau",
    "power bi", "cloud computing", "deep learning", "nlp", "ai", 
    "automation", "data analysis", "pandas"
}

# --------------------- UI SETUP ---------------------
st.set_page_config(page_title="Resume & Job Match Analyzer", page_icon="📄", layout="wide")

# Load custom styles
load_css()

# Display logo at the top (Centered)
display_logo()

# Title Section
st.title("📄 AI-Powered Resume & Job Match Analyzer 🚀")
st.write("Analyze your resume against job descriptions and receive insights on skill matching and improvement.")

# --------------------- SIDEBAR: FILE UPLOAD ---------------------
st.sidebar.header("📂 Upload Your Resume")
resume_file = st.sidebar.file_uploader("Upload a PDF Resume", type=["pdf"])

# Extract Resume Text & Display Below Title
resume_text = ""
if "resume_uploaded" not in st.session_state:
    st.session_state.resume_uploaded = False  # Keeps track of resume upload

if resume_file:
    st.session_state.resume_uploaded = True  # Mark that resume is uploaded

if st.session_state.resume_uploaded and resume_file:
    resume_text = extract_text_from_pdf(resume_file)
    with st.expander("📄 Extracted Resume Text (Click to Expand)", expanded=False):
        st.text_area("Resume Content", resume_text, height=250)

# --------------------- SIDEBAR: JOB DESCRIPTION ---------------------
st.sidebar.header("📜 Job Description")
job_description = st.sidebar.text_area("Paste the job description here")

# --------------------- ANALYZE MATCH BUTTON ---------------------
if st.sidebar.button("🔍 Analyze Match"):
    if not resume_file or not job_description:
        st.warning("⚠️ Please upload a resume and paste a job description before analyzing!")
    else:
        # Extract skills from both resume and job description
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)

        # Find Matching & Missing Skills
        matching_skills = job_skills & resume_skills
        missing_skills = job_skills - resume_skills

        # Categorize Missing Skills
        high_impact_missing = {skill for skill in missing_skills if skill in HIGH_IMPACT_SKILLS}
        low_impact_missing = missing_skills - high_impact_missing

        # Calculate Match Percentage
        match_percentage = (len(matching_skills) / len(job_skills) * 100) if job_skills else 0

        # --------------------- RESULTS SECTION ---------------------
        st.subheader("📊 Match Report")
        st.write(f"✅ **Matching Skills ({len(matching_skills)}):**")
        st.write(", ".join(matching_skills) if matching_skills else "None")

        if high_impact_missing:
            st.write(f"⚠️ **High-Impact Missing Skills ({len(high_impact_missing)}):**")
            st.write(", ".join(high_impact_missing))

        if low_impact_missing:
            st.write(f"🔸 **Low-Impact Missing Skills ({len(low_impact_missing)}):**")
            st.write(", ".join(low_impact_missing))

        # --------------------- MATCH SCORE ---------------------
        st.subheader("📈 Overall Match Score")
        st.progress(match_percentage / 100)
        st.write(f"🎯 Your resume matches **{match_percentage:.2f}%** of the job description.")

        # --------------------- RECOMMENDATIONS ---------------------
        st.subheader("📌 Recommendations for Improvement")
        
        if match_percentage < 50:
            st.error("🚨 Your resume does not align well with this job. Consider making major updates!")
        elif match_percentage < 80:
            st.warning("🛠 Your resume is a good match, but some key improvements are needed.")
        else:
            st.balloons()
            st.success("🎉 Great job! Your resume is well-aligned with the job description.")

        # High-Impact Skill Recommendations
        if high_impact_missing:
            st.subheader("🔹 High-Impact Skills to Improve")
            st.write("These skills are critical for this role and **should** be included in your resume.")
            for skill in high_impact_missing:
                st.write(f"🔹 **{skill.capitalize()}** - Try highlighting this skill in your experience or projects.")

        # Low-Impact Skill Recommendations
        if low_impact_missing:
            st.subheader("🔸 Low-Impact Skills to Improve")
            st.write("These skills are beneficial but not mandatory.")
            for skill in low_impact_missing:
                st.write(f"🔸 **{skill.capitalize()}** - Consider adding if relevant.")
