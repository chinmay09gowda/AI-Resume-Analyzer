import streamlit as st
from analyzer import analyze_resume
import plotly.express as px
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide"
)

# ---------------- SAFE UI STYLE ----------------
st.markdown("""
<style>

/* Navbar */
.navbar {
    background:#020617;
    padding:15px 30px;
    border-radius:12px;
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:30px;
}

.logo {
    font-size:24px;
    font-weight:bold;
    color:#38bdf8;
    font-family:"Times New Roman", serif;
}

.nav-btn {
    background:#1e293b;
    color:white;
    border:none;
    padding:8px 16px;
    border-radius:8px;
    margin-left:10px;
}

/* Headings */
h1, h2, h3 {
    font-family:"Times New Roman", serif;
}

/* Result box */
.result-box {
    background:#020617;
    padding:20px;
    border-radius:12px;
    border:1px solid #1e293b;
    margin-top:20px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
st.markdown("""
<div class="navbar">
    <div class="logo">AI Resume Analyzer</div>
    <div>
        <button class="nav-btn">Deploy</button>
        <button class="nav-btn">⋮</button>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("Upload your resume and receive AI career analysis")

# ---------------- FILE UPLOADER ----------------
uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

# ---------------- ANALYSIS ----------------
if uploaded_file:

    if st.button("Analyze Resume"):

        with st.spinner("Analyzing resume using AI..."):
            role, scores, missing_skills = analyze_resume(uploaded_file)

        st.success("Analysis Complete")

        col1, col2 = st.columns(2)

        # -------- Recommended Role --------
        with col1:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.subheader("Recommended Job Role")
            st.header(role)
            st.markdown('</div>', unsafe_allow_html=True)

        # -------- Missing Skills --------
        with col2:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.subheader("Missing Skills")

            if missing_skills:
                for skill in missing_skills:
                    st.write(f"• {skill}")
            else:
                st.write("No major skill gaps")

            st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- PIE CHART SECTION ----------------
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.subheader("Job Matching Scores")

        # Convert scores to dataframe
        chart_data = pd.DataFrame({
            "Job Role": list(scores.keys()),
            "Score": [round(v * 100, 2) for v in scores.values()]
        })

        # Sort roles by best match
        chart_data = chart_data.sort_values(by="Score", ascending=False)

        # Create donut pie chart
        fig = px.pie(
            chart_data,
            names="Job Role",
            values="Score",
            hole=0.5
        )

        # Show percentage + label
        fig.update_traces(
            textinfo="percent+label"
        )

        # Professional layout styling
        fig.update_layout(
            title="Role Match Distribution",
            title_x=0.5
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)