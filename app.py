import streamlit as st
import io

from contextlib import redirect_stdout
from scripts.variables import var
from main import contributors, commits, save_to_PDF
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

log_output = st.empty()  # Streamlit output area

# ---- ANALYZE BUTTON ----
if st.button("Analyze") and repo_input:
        var.repo = repo_input
        
        logger = Logger(use_streamlit=True, output_area=log_output)

        #st.subheader("📥 Analysis Output")    
        
            
        contributors(repo_input,log=logger,inline_display=False)
        commits(var)
        logger("✅ Data collection complete.")

'''
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
'''


