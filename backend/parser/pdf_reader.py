import fitz  # PyMuPDF

def extract_text_blocks(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    all_text_blocks = []

    for page_num, page in enumerate(doc):
        blocks = page.get_text("blocks")  # (x0, y0, x1, y1, text, block_no, ...)
        for b in blocks:
            block = {
                "page": page_num + 1,
                "x0": b[0],
                "y0": b[1],
                "x1": b[2],
                "y1": b[3],
                "text": b[4].strip()
            }
            all_text_blocks.append(block)

    return all_text_blocks
