import streamlit as st
import io

from contextlib import redirect_stdout
from scripts.variables import var
from main import contributors, commits
from scripts.helperFunctions import Logger

st.header("📊 GitHub Repo Analyzer",divider="rainbow")
repo_input = st.text_input("Enter GitHub repo:")


# Initialize session state
if "analyze_log" not in st.session_state:
    st.session_state.analyze_log = ""
if "pdf_log" not in st.session_state:
    st.session_state.pdf_log = ""
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

# === LAYOUT ORDER ===
subheader_placeholder = st.empty()       # For "📥 Analysis Output"
analyze_button_placeholder = st.empty()  # For Analyze button
log_output_container = st.container()    # For logs

# === STATIC UI ELEMENTS ===
subheader_placeholder.subheader("📥 Analysis Output")
analyze_clicked = analyze_button_placeholder.button("Analyze")

# === BUTTON LOGIC ===
if analyze_clicked and repo_input:
    var.repo = repo_input
    logger = Logger(use_streamlit=True, output_area=log_output_container)

    contributors(repo_input, log=logger, inline_display=False)
    commits(var)
    logger("✅ Data collection complete.")