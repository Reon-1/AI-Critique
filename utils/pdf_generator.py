import io
import unicodedata
from fpdf import FPDF
from .pdf_breaker import break_long_words

def clean_unicode_text(text: str) -> str:
    # Remove control characters except newline and tab
    return ''.join(ch for ch in text if unicodedata.category(ch)[0] != "C" or ch in '\n\t')

def generate_feedback_pdf(feedback_text: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(left=10, top=10, right=10)
    pdf.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=10)
    pdf.set_auto_page_break(auto=True, margin=15)

    # Clean and prepare text
    clean_text = feedback_text.replace("**", "").strip()
    clean_text = clean_unicode_text(clean_text)
    clean_text = clean_text.replace("•", "-").replace("‣", "-").replace("–", "-")
    clean_text = break_long_words(clean_text, max_len=50)

    usable_width = pdf.w - pdf.l_margin - pdf.r_margin
    print(f"Usable width: {usable_width} mm")  # Debug info, can be removed later

    clean_text = clean_text.replace('\r\n', '\n').replace('\r', '\n')

    # truncate long lines, replace non-rendered characters
    for line in clean_text.split('\n'):
        if not line.strip():
            continue  # Skip empty lines

        safe_line = line.strip()
        if len(safe_line) > 500:
            safe_line = safe_line[:500] + "..."

        try:
            pdf.multi_cell(0, 10, safe_line)
        except Exception as e:
            print(f"Error rendering line: {safe_line[:40]}... → {e}")
            fallback = ''.join(c if ord(c) < 128 else '?' for c in safe_line)
            try:
                pdf.multi_cell(0, 10, fallback)
            except Exception as e2:
                print(f"Failed fallback too: {e2}")


    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer.read()
