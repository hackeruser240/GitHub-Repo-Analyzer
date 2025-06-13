import streamlit as st
import io

from contextlib import redirect_stdout
from scripts.variables import var
from main import contributors,commits
from scripts.helperFunctions import Logger
from scripts.savetoPDF import save_to_PDF
from scripts.contributors import top_contributors_VIZ,lowest_contributors_VIZ

st.header("📊 GitHub Repo Analyzer",divider="rainbow")
repo_input = st.text_input("Enter GitHub repo:")


# === SESSION STATE INIT ===
if "analyze_log" not in st.session_state:
    st.session_state.analyze_log = []
if "pdf_log" not in st.session_state:
    st.session_state.pdf_log = []
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

# === LAYOUT ORDER ===
subheader_placeholder = st.empty()
analyze_button_placeholder = st.empty()
log_output_container = st.container(height=300)
pdf_button_placeholder = st.empty()
pdf_log_container = st.container(border=True)

# === STATIC ELEMENTS ===
subheader_placeholder.subheader("📥 Analysis Output")
analyze_clicked = analyze_button_placeholder.button("Analyze")

# === ANALYZE BUTTON LOGIC ===
if analyze_clicked and repo_input:
    var.repo = repo_input
    logger = Logger(use_streamlit=True, output_area=log_output_container)

    try:
        contributors(repo_input, log=logger, inline_display=False)
        commits(var)
        logger("✅ Data collection complete.")
    except Exception as e:
        print(f"Error @ Point 1:\n{e}")


    st.session_state.analyze_log = logger.get_logs()  # Persist logs
    st.session_state.analyzed = True

elif analyze_clicked and not repo_input:
    st.warning("Please input a repo name")

# === SHOW PLOT AFTER ANALYSIS ===
if st.session_state.analyzed:
    with st.container():
        top_contributors_VIZ(var.contributors_data, use_streamlit=True, st_output_area=None)

    with st.container():
        lowest_contributors_VIZ(var.contributors_data, use_streamlit=True, st_output_area=None)

# === RENDER ANALYZE LOG (ALWAYS SHOW)
with log_output_container:
    for line in st.session_state.analyze_log:
        st.markdown(line)

# === GENERATE PDF BUTTON ===
if st.session_state.analyzed:
    if st.button("Generate PDF"):
        logger = Logger(use_streamlit=True, output_area=None)  # No output area
        save_to_PDF(var, log=logger)
        logger("📄 PDF generated and saved.")
        st.session_state.pdf_log = logger.get_logs()

# === RENDER PDF LOG
if st.session_state.pdf_log:
    st.subheader("📄 PDF Generation Output")
    with st.container(border=True):
        for line in st.session_state.pdf_log:
            st.markdown(line)