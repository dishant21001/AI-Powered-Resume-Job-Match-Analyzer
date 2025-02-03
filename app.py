import streamlit as st
import os
import base64
import pandas as pd
from collections import Counter
from utils.text_processing import extract_text_from_pdf
from utils.skills_extractor import extract_skills

# --------------------- LOAD CUSTOM STYLES ---------------------
def load_css():
    css_file_path = "assets\styles.css"
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
            <div style="display: flex; justify-content: center; align-items: center; padding: 20px;">
                <img src="data:image/png;base64,{encoded_logo}" width="200">
            </div>
            """,
            unsafe_allow_html=True
        )

# --------------------- CONFIGURATION ---------------------
st.set_page_config(page_title="AI Resume & Job Match Analyzer", page_icon="assets/logo.png", layout="wide")

# Load custom styles
load_css()

# --------------------- MAIN CONTAINER ---------------------
with st.container():
    display_logo()
    st.markdown(
        """
        <div class="header-container">
            <h1 class="main-title">📄 AI-POWERED RESUME & JOB MATCH ANALYZER 🚀</h1>
            <p class="subtitle">Analyze your resume against job descriptions and receive insights on skill matching and improvement.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------- SIDEBAR: FILE UPLOAD & JOB POSITION ---------------------
st.sidebar.header("📂 Upload Your Resume")
resume_file = st.sidebar.file_uploader("Upload a PDF Resume", type=["pdf"])

st.sidebar.header("📝 Enter the Position Title")
job_position = st.sidebar.text_input("Enter the job title (e.g., Data Analyst, Software Engineer)", "")

st.sidebar.header("📜 Job Description")
job_description = st.sidebar.text_area("Paste the job description here")

resume_text = ""
if "resume_uploaded" not in st.session_state:
    st.session_state.resume_uploaded = False

if resume_file:
    st.session_state.resume_uploaded = True

if st.session_state.resume_uploaded and resume_file:
    resume_text = extract_text_from_pdf(resume_file)
    with st.expander("📄 Extracted Resume Text (Click to Expand)", expanded=False):
        st.text_area("Resume Content", resume_text, height=250)

# --------------------- ANALYZE MATCH BUTTON ---------------------
if st.sidebar.button("🔍 Analyze Match"):
    if not resume_file or not job_description or not job_position:
        st.warning("⚠️ Please upload a resume, enter the job title, and paste a job description before analyzing!")
    else:
        # Extract skills from resume and job description
        resume_skills = extract_skills(resume_text)
        job_skills_list = extract_skills(job_description)

        # Prioritize extracting **skills relevant to the entered job position**
        job_skills_freq = Counter(job_skills_list)
        job_skills = set(job_skills_list)

        # Determine high-impact & low-impact skills dynamically
        sorted_skills = sorted(job_skills_freq.items(), key=lambda x: x[1], reverse=True)
        high_impact_threshold = max(2, len(sorted_skills) // 3)  # Top third as high-impact

        high_impact_skills = {skill for skill, count in sorted_skills[:high_impact_threshold]}
        low_impact_skills = job_skills - high_impact_skills

        # Identify missing skills
        matching_skills = job_skills & resume_skills
        missing_skills = job_skills - resume_skills

        high_impact_missing = missing_skills & high_impact_skills
        low_impact_missing = missing_skills & low_impact_skills

        match_percentage = (len(matching_skills) / len(job_skills) * 100) if job_skills else 0

        # --------------------- RESULTS SECTION ---------------------
        st.subheader(f"📊 Match Report for **{job_position}**")
        st.write(f"✅ **Matching Skills ({len(matching_skills)}):**")
        st.write(", ".join(matching_skills) if matching_skills else "None")

        if missing_skills:
            st.subheader("🚨 Missing Skills")
            st.write(f"These skills are required for the **{job_position}** role but are missing from your resume.")

            cols = st.columns(4)  # Creates a 4-column layout
            for index, skill in enumerate(missing_skills):
                with cols[index % 4]:  
                    st.markdown(f"- {skill}")

        if high_impact_missing:
            st.markdown("### 🔹 High-Impact Skills to Improve")
            st.write("These skills are **critical** for the role and should be included in your resume.")

            cols = st.columns(4)  
            for index, skill in enumerate(high_impact_missing):
                with cols[index % 4]:  
                    st.markdown(f"- {skill}")

        if low_impact_missing:
            st.markdown("### 🔸 Low-Impact Skills to Improve")
            st.write("These skills are beneficial but not mandatory.")

            cols = st.columns(4)  
            for index, skill in enumerate(low_impact_missing):
                with cols[index % 4]:  
                    st.markdown(f"- {skill}")

        # --------------------- MATCH SCORE ---------------------
        st.subheader("📈 Overall Match Score")
        st.progress(match_percentage / 100)
        st.write(f"🎯 Your resume matches **{match_percentage:.2f}%** of the **{job_position}** job description.")

        # --------------------- RECOMMENDATIONS ---------------------
        # --------------------- RECOMMENDATIONS ---------------------
        # --------------------- RECOMMENDATIONS ---------------------
# --------------------- RECOMMENDATIONS ---------------------
    st.subheader("📌 Recommendations for Improvement")

    import random

    if match_percentage < 50:
        # Generate multiple sad faces spread around the center
        sad_faces_html = ""
        num_sad_faces = 12  # Number of falling sad faces

        for i in range(num_sad_faces):
            left_position = random.randint(40, 60)  # Spread them in the center range (40% - 60%)
            delay = round(random.uniform(0.3, 2.5), 2)  # Random delay (0.3s – 2.5s)
            fall_duration = round(random.uniform(2.5, 4), 2)  # Random fall speed (2.5s – 4s)
            sad_faces_html += f"""
            <div class="falling-sad" style="left: {left_position}%; animation-delay: {delay}s; animation-duration: {fall_duration}s;">😞</div>
            """

        st.markdown(
            f"""
            <style>
            @keyframes fall {{
                0% {{ transform: translateY(-50px); opacity: 1; }}
                100% {{ transform: translateY(100vh); opacity: 0; }}
            }}
            .falling-sad {{
                position: fixed;
                top: 0;
                font-size: 40px;
                animation: fall linear 1; /* Runs only ONCE */
            }}
            </style>
            {sad_faces_html}
            <div style='background-color:#ffcccc; padding:15px; border-radius:10px; font-size:16px; text-align:center;'>
            🚨 <strong>Your resume does not align well with this job.</strong> Consider making major updates!
            </div>
            """, unsafe_allow_html=True
        )
        st.error("⚠️ Major improvements needed! Focus on missing high-impact skills.")




    elif match_percentage < 80:
        st.markdown(
            """
            <div style='background-color:#fff3cd; padding:15px; border-radius:10px; font-size:16px;'>
            🛠 <strong>Your resume is a good match, but some key improvements are needed.</strong>
            </div>
            """, unsafe_allow_html=True
        )
        st.snow()  # Light snowfall effect for motivation
        st.warning("🔍 Consider optimizing missing high-impact skills!")

    else:
        st.balloons()
        st.markdown(
            """
            <div style='background-color:#d4edda; padding:15px; border-radius:10px; font-size:16px;'>
            🎉 <strong>Great job!</strong> Your resume is well-aligned with the job description.
            </div>
            """, unsafe_allow_html=True
        )
        st.success("✅ Strong resume match!")

