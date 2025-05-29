import streamlit as st
import io

from contextlib import redirect_stdout
from scripts.variables import var
from main import contributors, commits, save_to_PDF

st.header("📊 GitHub Repo Analyzer",divider="white")
repo_input = st.text_input("Enter GitHub repo:")

# Initialize session state
if "analyze_log" not in st.session_state:
    st.session_state.analyze_log = ""
if "pdf_log" not in st.session_state:
    st.session_state.pdf_log = ""
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False


# ---- ANALYZE BUTTON ----
if st.button("Analyze"):
    if repo_input:
        var.repo = repo_input

        # Capture print logs
        f = io.StringIO()
        with redirect_stdout(f):
            contributors(repo_input,inline_display=True)
            commits(var)
            print("✅ Data collection complete.")

        st.session_state.analyze_log = f.getvalue()
        st.session_state.analyzed = True


# ---- SHOW ANALYZE OUTPUT ----
if st.session_state.analyze_log:
    st.subheader("📥 Analysis Output")
    st.code(st.session_state.analyze_log, language="text")


# ---- GENERATE PDF BUTTON ----
if st.session_state.analyzed:
    if st.button("Generate PDF"):
        f = io.StringIO()
        with redirect_stdout(f):
            save_to_PDF(var)
            print("📄 PDF generated and saved.")

        st.session_state.pdf_log = f.getvalue()


# ---- SHOW PDF OUTPUT ----
if st.session_state.pdf_log:
    st.subheader("📄 PDF Generation Output")
    st.code(st.session_state.pdf_log, language="text")
