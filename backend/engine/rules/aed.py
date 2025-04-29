import re

def check_nsn_present(text_blocks):
    all_text = " ".join([b["text"].upper() for b in text_blocks])
    found = re.search(r"\bNSN[:\s]*\d{4}-\d{2}-\d{6}\b", all_text)
    return {
        "rule": "NSN Number Present",
        "passed": found is not None
    }

def check_drawing_classification(text_blocks):
    keywords = ["INSTALLATION", "SCHEMATIC", "WIRING", "DETAIL", "OUTLINE", "BLOCK DIAGRAM"]
    all_text = " ".join([b["text"].upper() for b in text_blocks])
    found = any(k in all_text for k in keywords)
    return {
        "rule": "Drawing Type Specified",
        "passed": found
    }

def check_mil_std_citations(text_blocks):
    standards = ["MIL-STD-100", "MIL-STD-129", "MIL-STD-31000"]
    all_text = " ".join([b["text"].upper() for b in text_blocks])
    found = any(std in all_text for std in standards)
    return {
        "rule": "MIL-STD Reference Present",
        "passed": found
    }

def check_revision_format(text_blocks):
    all_text = " ".join([b["text"].upper() for b in text_blocks])
    pattern = r"\b(REV|REVISION)[\s-]*(?:[A-Z]|\d+)\b"
    found = re.search(pattern, all_text)
    return {
        "rule": "Revision Format Valid",
        "passed": found is not None
    }

def check_tolerance_dimensions(text_blocks):
    all_text = " ".join([b["text"] for b in text_blocks])
    found = re.search(r"\d+(\.\d+)?\s*±\s*\d+(\.\d+)?", all_text)
    return {
        "rule": "Tolerances Present with Dimensions",
        "passed": found is not None
    }

def check_units_specified(text_blocks):
    units = ["IN", "INCH", "MM", "FEET", "MILLIMETERS"]
    all_text = " ".join([b["text"].upper() for b in text_blocks])
    found = any(unit in all_text for unit in units)
    return {
        "rule": "Measurement Units Declared",
        "passed": found
    }

def check_security_notice(text_blocks):
    keywords = ["SECURITY NOTICE", "WARNING", "PROPRIETARY", "EXPORT CONTROLLED"]
    all_text = " ".join([b["text"].upper() for b in text_blocks])
    found = any(k in all_text for k in keywords)
    return {
        "rule": "Security Notice Present",
        "passed": found
    }

def check_unique_id_present(text_blocks):
    all_text = " ".join([b["text"].upper() for b in text_blocks])
    found = re.search(r"\bUID[:\s]*[A-Z0-9\-]+\b", all_text)
    return {
        "rule": "Unique Identifier Code Present",
        "passed": found is not None
    }

# 📦 Collect all AED rules
rules = [
    check_nsn_present,
    check_drawing_classification,
    check_mil_std_citations,
    check_revision_format,
    check_tolerance_dimensions,
    check_units_specified,
    check_security_notice,
    check_unique_id_present,
]
