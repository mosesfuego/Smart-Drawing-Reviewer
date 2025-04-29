from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from parser.pdf_reader import extract_text_blocks
from engine.rules import check_required_fields
from engine.rules import run_all_rules
import json

import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(page_title="Drawing Reviewer", layout="wide")

st.title("📐 Drawing Reviewer MVP")

uploaded_file = st.file_uploader("Upload a drawing PDF", type=["pdf"])

if uploaded_file:
    st.success("File uploaded successfully!")

    reader = PdfReader(uploaded_file)
    page = reader.pages[0]
    raw_text = page.extract_text()

    # Convert raw text into blocks format expected by rules
    text_blocks = [{"text": raw_text, "y0": 0, "y1": 1000}]  # Simple block format

    st.subheader("🔍 Raw Extracted Text")
    st.text(raw_text[:1000])  # preview first 1000 chars

    with st.spinner("Running rule checks..."):
        results = run_all_rules(text_blocks)

    st.subheader("✅ Rule Check Results")
    for result in results:
        status = "✅" if result["passed"] else "❌"
        st.markdown(f"{status} **{result['rule']}**")
        if not result["passed"]:
            if "missing_fields" in result:
                st.markdown("Missing fields: " + ", ".join(result["missing_fields"]))
            elif "error" in result:
                st.markdown(f"Error: {result['error']}")

    # Summary
    passed_count = sum(1 for r in results if r["passed"])
    total_count = len(results)
    st.info(f"Passed {passed_count} out of {total_count} checks")
