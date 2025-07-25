# app1.py
import streamlit as st

st.set_page_config(page_title="Agentic Review Terminal Output", layout="centered")
st.title("🧠 Agentic Review Terminal Output Viewer")
st.markdown("This app displays the latest review output from your terminal.")

# Path to the log file where your Flask app prints the review result
log_file = st.text_input("Path to log file (e.g. agentic_review.log):", value="agentic_review.log")

if st.button("Show Latest Review Output"):
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        # Find the last line containing 'Agentic workflow result:'
        review_lines = [line for line in lines if "Agentic workflow result:" in line]
        if review_lines:
            st.success("✅ Latest Agentic Review Output:")
            st.code(review_lines[-1], language="text")
        else:
            st.info("No agentic review output found in the log file yet.")
    except Exception as e:
        st.error(f"Error reading log file: {e}")

st.markdown("---")
st.markdown("**Note:** To use this, configure your Flask app to write review results to the specified log file.")
