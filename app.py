import streamlit as st 
from scripts.variables import var
from main import contributors,commits,save_to_PDF

st.title("📊 GitHub Repo Analyzer")

repo_input = st.text_input("Enter GitHub repo (e.g., facebook/react)")

# Check if analyze has been clicked before
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

if st.button("Analyze"):
    if repo_input:
        var.repo = repo_input
        contributors(repo_input)
        commits(var)
        st.session_state.analyzed = True
        st.success("✅ Data collected!")

# If data was analyzed, show the next step
if st.session_state.analyzed:
    if st.button("Generate PDF"):
        save_to_PDF(var)
        st.info("📄 PDF generated and saved.")