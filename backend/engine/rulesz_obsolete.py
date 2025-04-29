import re

def check_required_fields(text_blocks):
    required_keywords = [
        "DRAWING NUMBER",
        "TITLE",
        "SCALE",
        "DATE",
        "APPROVED",
        "DRAWN BY",
        "REV"
    ]

    missing_fields = []

    all_text = " ".join([b["text"].upper() for b in text_blocks])

    for keyword in required_keywords:
        if keyword not in all_text:
            missing_fields.append(keyword)

    return {
        "rule": "Basic Title Block Completeness",
        "passed": len(missing_fields) == 0,
        "missing_fields": missing_fields
    }
def check_revision_present(text_blocks):
    all_text = " ".join([b["text"].upper() for b in text_blocks])
    found = "REV" in all_text or "REVISION" in all_text
    return {
        "rule": "Revision Label Present",
        "passed": found
    }
def check_scale_valid(text_blocks):
    all_text = " ".join([b["text"].upper() for b in text_blocks])
    found = "SCALE" in all_text and ("1:" in all_text or "NTS" in all_text)
    return {
        "rule": "Drawing Scale Valid",
        "passed": found
    }

def check_sheet_numbering(text_blocks):
    pattern = r"SHEET\s+\d+\s+OF\s+\d+"
    all_text = " ".join([b["text"].upper() for b in text_blocks])
    match = re.search(pattern, all_text)
    return {
        "rule": "Sheet Numbering Present",
        "passed": match is not None
    }

def check_date_format(text_blocks):
    all_text = " ".join([b["text"] for b in text_blocks])
    date_patterns = [
        r"\d{2}/\d{2}/\d{2,4}",      # 01/12/2023 or 01/12/23
        r"\d{2}-\d{2}-\d{2,4}",      # 01-12-2023
        r"\d{4}-\d{2}-\d{2}",        # 2023-12-01
    ]
    found = any(re.search(p, all_text) for p in date_patterns)
    return {
        "rule": "Date Format Valid",
        "passed": found
    }
def check_units_consistency(text_blocks):
    all_text = " ".join([b["text"].upper() for b in text_blocks])
    passed = any(u in all_text for u in ["MM", "IN", "INCHES", "MILLIMETERS"])
    return {
        "rule": "Units Mentioned",
        "passed": passed
    }
def check_title_block_location(text_blocks):
    bottom_blocks = [b for b in text_blocks if b["y0"] > 700]  # You can tune this
    keywords = ["DRAWN", "TITLE", "SCALE", "REV", "DATE"]
    found = any(kw in b["text"].upper() for kw in keywords for b in bottom_blocks)
    
    return {
        "rule": "Title Block Positioned Near Bottom",
        "passed": found
    }
def check_pdf_is_machine_readable(text_blocks):
    passed = len(text_blocks) > 10  # Anything below 10 is suspicious
    return {
        "rule": "PDF is Machine-Readable",
        "passed": passed
    }
from collections import Counter
import re

# 9. Duplicate Fields
def check_duplicate_fields(text_blocks):
    keywords = ["TITLE", "DRAWING NUMBER", "SCALE", "DATE", "REV", "APPROVED"]
    field_counts = Counter()
    for block in text_blocks:
        for kw in keywords:
            if kw in block["text"].upper():
                field_counts[kw] += 1
    duplicates = [kw for kw, count in field_counts.items() if count > 1]
    return {
        "rule": "Duplicate Field Check",
        "passed": len(duplicates) == 0,
        "duplicates": duplicates
    }

# 10. Field Alignment Heuristic
def check_field_alignment_heuristic(text_blocks):
    target_fields = ["TITLE", "DRAWN", "DATE", "SCALE", "REV"]
    y_coords = []
    for block in text_blocks:
        for field in target_fields:
            if field in block["text"].upper():
                y_coords.append(block["y0"])
    passed = len(y_coords) < 2 or max(y_coords) - min(y_coords) < 50
    return {
        "rule": "Field Alignment Heuristic",
        "passed": passed,
        "y_range": (min(y_coords, default=0), max(y_coords, default=0))
    }

# 11. General Notes Present
def check_notes_block_present(text_blocks):
    keywords = [
        "UNLESS OTHERWISE SPECIFIED",
        "ALL DIMENSIONS IN",
        "TOLERANCES",
        "FINISH",
        "BREAK SHARP EDGES"
    ]
    all_text = " ".join([b["text"].upper() for b in text_blocks])
    found_notes = [kw for kw in keywords if kw in all_text]
    return {
        "rule": "General Notes Present",
        "passed": len(found_notes) > 0,
        "found": found_notes
    }

# 12. Sheet Label Consistency
def check_sheet_label_consistency(text_blocks):
    sheet_matches = []
    for b in text_blocks:
        match = re.search(r"SHEET\s+(\d+)\s+OF\s+(\d+)", b["text"].upper())
        if match:
            current, total = int(match.group(1)), int(match.group(2))
            sheet_matches.append((current, total))
    consistent = all(curr <= total for curr, total in sheet_matches)
    return {
        "rule": "Sheet Label Consistency",
        "passed": consistent,
        "found": sheet_matches
    }

# 13. Tolerance Format Valid
def check_tolerance_format(text_blocks):
    all_text = " ".join([b["text"] for b in text_blocks])
    patterns = [
        r"±\s*\d+\.\d+",       # ±0.01
        r"\+\d+\.\d+\s*/\s*-\d+\.\d+",  # +0.1/-0.0
        r"\+\d+\.\d+\s*-\d+\.\d+"       # +0.1 -0.0
    ]
    found = any(re.search(p, all_text) for p in patterns)
    return {
        "rule": "Tolerance Format Valid",
        "passed": found
    }

# 14. Font Size Legibility
def check_font_size_legibility(text_blocks):
    heights = [b["y1"] - b["y0"] for b in text_blocks]
    tiny_texts = [h for h in heights if h < 11]  # 11 px ≈ 8pt
    too_small_ratio = len(tiny_texts) / len(heights) if heights else 0
    passed = too_small_ratio < 0.3
    return {
        "rule": "Font Size Legibility",
        "passed": passed,
        "too_small_ratio": round(too_small_ratio, 2)
    }

# 15. GD&T Symbols Present
def check_geometric_symbols_present(text_blocks):
    gdnt_symbols = ["Ⓜ", "Ⓟ", "Ⓣ", "ⓨ", "⓴"]
    found = any(any(sym in b["text"] for sym in gdnt_symbols) for b in text_blocks)
    return {
        "rule": "GD&T Symbols Present",
        "passed": found
    }

# 16. Drawing Number Format
def check_drawing_number_format(text_blocks):
    patterns = [
        r"(DWG[-\s]*\d+[A-Z]?)",     # DWG-1234A
        r"(P/N[-\s]*\d{4,})"         # P/N 45678
    ]
    all_text = " ".join([b["text"].upper() for b in text_blocks])
    found = any(re.search(p, all_text) for p in patterns)
    return {
        "rule": "Drawing Number Format Valid",
        "passed": found
    }
#UPDATE TO INCLUDE DIFFERENT RULESETS
rule_sets = {
    "ASME Y14": [...],
    "AED-1": [rule_1, rule_2, ..., rule_10]
}

def run_all_rules(text_blocks):
    checks = [
        check_required_fields,
        check_revision_present,
        check_scale_valid,
        check_date_format,
        check_units_consistency,
        check_title_block_location,
        check_duplicate_fields,
        check_field_alignment_heuristic,
        check_notes_block_present,
        check_sheet_label_consistency,
        check_tolerance_format,
        check_font_size_legibility,
        check_geometric_symbols_present,
        check_drawing_number_format,
        check_pdf_is_machine_readable
    ]

    results = []
    for rule_func in checks:
        try:
            result = rule_func(text_blocks)
            results.append(result)
        except Exception as e:
            results.append({
                "rule": rule_func.__name__,
                "passed": False,
                "error": str(e)
            })

    return results



