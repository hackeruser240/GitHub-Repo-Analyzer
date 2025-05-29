import streamlit as st
import io
import sys
from contextlib import redirect_stdout

from scripts.variables import var
from main import contributors, commits, save_to_PDF

st.title("📊 GitHub Repo Analyzer")

repo_input = st.text_input("Enter GitHub repo (e.g., facebook/react)")

# Flag to track state
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

# Set up a placeholder to show logs
log_output = st.empty()

if st.button("Analyze"):
    if repo_input:
        var.repo = repo_input

        # Redirect print statements
        f = io.StringIO()
        with redirect_stdout(f):
            contributors(repo_input)
            commits(var)
            print("✅ Data collection complete.")

        st.session_state.analyzed = True

        # Show logs in the Streamlit UI
        log_output.code(f.getvalue(), language="text")

# Show Generate PDF only if data was analyzed
if st.session_state.analyzed:
    if st.button("Generate PDF"):
        f = io.StringIO()
        with redirect_stdout(f):
            save_to_PDF(var)
            print("📄 PDF generated and saved.")

        log_output.code(f.getvalue(), language="text")
