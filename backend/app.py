import streamlit as st
from PyPDF2 import PdfReader
from engine.rules.aed import rules as aed_rules
from engine.rules.asme import rules as asme_rules

rule_sets = {
    "AED": aed_rules,
    "ASME Y14": asme_rules,
}



st.set_page_config(page_title="Drawing Reviewer", layout="wide")

# 💡 Sidebar
with st.sidebar:
    st.title("🛠️ Settings")
    st.write("Configure your rule check preferences here.")
    show_raw = st.checkbox("Show Raw PDF Text", value=True)
    rule_set = st.selectbox("Select Rule Set", ["AED", "ASME Y14"])
selected_rules = rule_sets.get(rule_set, [])
# 🎯 Title
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>📐 AI Drawing Reviewer</h1>
    <h4 style='text-align: center; color: gray;'>Upload engineering drawings and receive instant rule-based feedback.</h4>
    """,
    unsafe_allow_html=True
)

# 📤 File uploader
uploaded_file = st.file_uploader("### 📎 Upload a Drawing (PDF)", type=["pdf"], label_visibility="collapsed")

if uploaded_file:
    st.success("✅ File uploaded successfully!")

    reader = PdfReader(uploaded_file)
    page = reader.pages[0]
    raw_text = page.extract_text()

    if show_raw:
        with st.expander("🧾 Raw Extracted Text (Page 1)", expanded=False):
            st.text(raw_text[:2000] if raw_text else "[No text detected]")

    with st.spinner("🔍 Running rule checks..."):
        # Convert raw text into blocks format expected by rules
        text_blocks = [{"text": raw_text or "", "y0": 0, "y1": 1000}]
        
        # Select rules based on user choice
        selected_rules = aed_rules if rule_set == "AED" else asme_rules
        
        # Run all rules
        results = []
        for rule_func in selected_rules:
            try:
                result = rule_func(text_blocks)
                results.append(result)
            except Exception as e:
                results.append({
                    "rule": rule_func.__name__,
                    "passed": False,
                    "error": str(e)
                })

    st.markdown("## 🧠 Rule Check Results")

    # Convert results to the expected format
    issues = []
    for result in results:
        if not result["passed"]:
            problem = ""
            if "missing_fields" in result:
                problem = f"Missing fields: {', '.join(result['missing_fields'])}"
            elif "error" in result:
                problem = f"Error: {result['error']}"
            else:
                problem = "Check failed"
            
            issues.append({
                "rule": result["rule"],
                "problem": problem
            })

    if issues:
        st.markdown("### ❌ Failed Checks")
        for issue in issues:
            st.markdown(
                f"""
                <div style='
                    border: 1px solid #ff4d4d;
                    border-left: 6px solid #ff1a1a;
                    padding: 1rem;
                    border-radius: 8px;
                    margin-bottom: 1rem;
                    background-color: #1f1d1d;
                    box-shadow: 0 2px 4px rgba(255, 0, 0, 0.1);
                '>
                    <h5 style='margin: 0; color: #ff4d4d; font-weight: bold;'>🔴 {issue['rule']}</h5>
                    <p style='margin: 0.5rem 0 0 0; color: #cccccc;'>{issue['problem']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.success("🎉 All rules passed! No issues found.")

else:
    st.info("👈 Upload a PDF to begin analysis.")