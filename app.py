import streamlit as st
import pandas as pd
import time
import io
import hashlib
import json
import PyPDF2  # Mock placeholder
import docx  # Mock placeholder
import unittest

# Mock OpenAI/Hugging Face APIs
def mock_openai_summarize(transcript, api_key=None):
    words = transcript.split()
    summary_length = max(50, len(words) // 10)
    return " ".join(words[:summary_length]) + " [...] (Summary truncated)"

def mock_contract_analyzer(contract):
    clauses = ["Liability", "Termination", "Payment", "Confidentiality"]
    return [
        {
            "clause": c,
            "risk": "High" if c in ["Liability", "Confidentiality"] else "Low",
            "score": 0.9 if c in ["Liability", "Confidentiality"] else 0.5,
            "suggestion": "Limit exposure to $100K" if c == "Liability" else "Standard clause"
        } for c in clauses
    ]

def mock_case_research(query):
    if not query.strip():
        return [{"error": "Empty query, please enter a valid search term"}]
    parsed_query = query.lower().split(",")[0].strip()
    return [
        {"case": "Smith v. Jones, 2023", "summary": f"{parsed_query} upheld due to breach", "relevance": 0.85},
        {"case": "Doe v. Roe, 2022", "summary": f"{parsed_query} dismissed", "relevance": 0.75}
    ]

# Mock Stripe subscription
def mock_stripe_subscribe(user_id):
    return {"status": "active", "plan": "unlimited", "cost": "$99/month"}

# Mock file parsing
def mock_parse_file(file, file_type):
    if file_type == "pdf":
        return "Sample transcript text " * 100
    elif file_type == "docx":
        return "Sample transcript text " * 100
    return ""

# Streamlit app
st.set_page_config(page_title="Lexinary AI", page_icon="⚖️", layout="wide")
st.title("⚖️ Lexinary AI: Next-Generation Legal Automation")
st.markdown("""
Sophisticated AI for small law firms. Summarize depositions, analyze contracts, and accelerate case research.  
**Free to test (3 summaries), $99/month for unlimited.**  
Built by Grok for legal innovation.
""", unsafe_allow_html=True)
st.markdown('<style>h1 {color: #1E3A8A; font-family: "Arial", sans-serif;} body {background: linear-gradient(to right, #E0F2FE, #DBEAFE);} .stButton>button {background: #1E3A8A; color: white; border-radius: 5px; box-shadow: 0 0 10px #1E90FF;} .sidebar {position: sticky; top: 0;}</style>', unsafe_allow_html=True)

# Mock user authentication
if "user_id" not in st.session_state:
    st.session_state.user_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
    st.session_state.summary_count = 0
    st.session_state.analytics = {"summaries": 0, "contracts": 0, "research": 0, "time_spent": 0}
    st.session_state.start_time = time.time()
    st.session_state.subscribed = False

# Subscription modal
if st.session_state.summary_count >= 3 and not st.session_state.subscribed:
    st.markdown('<div style="background: #FFE4E1; padding: 10px; border-radius: 5px;">Free limit reached! Subscribe for $99/month: [Sign Up](#) (Mock link)</div>', unsafe_allow_html=True)
    if st.button("Subscribe Now", key="subscribe"):
        st.session_state.subscribed = True
        st.session_state.analytics["subscribed"] = mock_stripe_subscribe(st.session_state.user_id)
        st.success("Subscribed to unlimited plan! (Mock)")

# Input form
st.header("Analyze Your Legal Documents")
with st.expander("Deposition Summarizer", expanded=True):
    uploaded_file = st.file_uploader("Upload Transcript (PDF/Word)", type=["pdf", "docx"], help="Max 10MB")
    if uploaded_file:
        if uploaded_file.size > 10 * 1024 * 1024:
            st.error("File too large. Max size: 10MB.", icon="🚨")
        else:
            file_type = uploaded_file.type.split("/")[-1]
            transcript = mock_parse_file(uploaded_file, file_type)
            st.write(f"Uploaded: {uploaded_file.name}")
            if st.session_state.summary_count >= 3 and not st.session_state.subscribed:
                st.error("Free limit reached (3 summaries). Subscribe for $99/month!", icon="🔒")
            elif st.button("Generate Summary", key="summarize"):
                st.session_state.summary_count += 1
                st.session_state.analytics["summaries"] += 1
                with st.spinner("Summarizing transcript..."):
                    progress = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress.progress(i + 1)
                    summary = mock_openai_summarize(transcript)
                    st.success(f"Summary generated! (Summary {st.session_state.summary_count}/3 free)")
                    st.subheader("Deposition Summary")
                    with st.expander("Preview (First 100 chars)"):
                        st.write(summary[:100] + "...")
                    st.write(summary)
                    st.download_button(
                        label="Download Summary",
                        data=summary,
                        file_name=f"summary_{st.session_state.user_id}.txt",
                        mime="text/plain"
                    )
                    if not st.session_state.subscribed:
                        st.info(f"Summaries left: {3 - st.session_state.summary_count}/3 free.")
with st.expander("Contract Analyzer"):
    contract_text = st.text_area("Paste Contract Text", help="Max 5000 words")
    if contract_text and len(contract_text.split()) > 5000:
        st.error("Contract text too long. Max 5000 words.", icon="🚨")
    elif contract_text and st.button("Analyze Contract", key="analyze"):
        st.session_state.analytics["contracts"] += 1
        with st.spinner("Analyzing contract..."):
            time.sleep(1)
            analysis = mock_contract_analyzer(contract_text)
            st.success("Contract analyzed!")
            st.subheader("Contract Analysis")
            st.json(analysis)
            st.download_button(
                label="Download Analysis (JSON)",
                data=json.dumps(analysis, indent=2),
                file_name=f"contract_analysis_{st.session_state.user_id}.json",
                mime="application/json"
            )
with st.expander("Case Research"):
    query = st.text_input("Enter Case Research Query (e.g., 'negligence, New Hampshire')", help="Search for case law")
    if query and st.button("Search Cases", key="research"):
        st.session_state.analytics["research"] += 1
        with st.spinner("Searching cases..."):
            time.sleep(1)
            results = mock_case_research(query)
            st.success("Cases found!")
            st.subheader("Case Research Results")
            st.json(results)

# Analytics
st.session_state.analytics["time_spent"] = int(time.time() - st.session_state.start_time)
with st.sidebar.expander("Usage Analytics"):
    st.write(f"Summaries: {st.session_state.analytics['summaries']}")
    st.write(f"Contracts Analyzed: {st.session_state.analytics['contracts']}")
    st.write(f"Case Searches: {st.session_state.analytics['research']}")
    st.write(f"Time Spent: {st.session_state.analytics['time_spent']} seconds")
    if st.session_state.subscribed:
        st.write(f"Subscription: {st.session_state.analytics['subscribed']['plan']}")

# Sidebar
st.sidebar.header("How to Use Lexinary AI")
st.sidebar.markdown("""
1. Upload a transcript, paste contract text, or enter a case query.
2. Click 'Generate Summary,' 'Analyze Contract,' or 'Search Cases.'
3. Download results for your case.
**Tip**: Try a 10-page transcript, 500-word contract, or 'negligence' query.
**Next steps**: Approve MVP on September 10, 2025!
""")

# Footer
st.markdown("---")
st.write(f"Lexinary AI v0.8 | Built by Grok | August 11, 2025 | User ID: {st.session_state.user_id}")

# Unit tests for GitHub Actions
class TestLexinaryAI(unittest.TestCase):
    def test_summarize(self):
        result = mock_openai_summarize("test " * 100)
        self.assertTrue(len(result.split()) >= 50)

    def test_contract_analyzer(self):
        result = mock_contract_analyzer("test contract")
        self.assertEqual(len(result), 4)

    def test_case_research(self):
        result = mock_case_research("negligence")
        self.assertTrue(len(result) >= 1)
        result = mock_case_research("")
        self.assertTrue("error" in result[0])

if __name__ == "__main__":
    unittest.main()
