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
    pdf.set_font("DejaVu", size=12)
    pdf.set_auto_page_break(auto=True, margin=15)

    # Clean and prepare text
    clean_text = feedback_text.replace("**", "").strip()
    clean_text = clean_unicode_text(clean_text)
    clean_text = break_long_words(clean_text, max_len=50)

    usable_width = pdf.w - pdf.l_margin - pdf.r_margin
    print(f"Usable width: {usable_width} mm")  # Debug info, can be removed later

    # Write lines with safety checks
    for line in clean_text.split('\n'):
        if line.strip():  # skip empty or whitespace-only lines
            try:
                pdf.multi_cell(0, 10, line)
            except Exception as e:
                print(f"Error printing line: {line[:30]}... - {e}")
                # Try printing a truncated version instead of failing
                truncated = line[:100] + "..." if len(line) > 100 else line
                try:
                    pdf.multi_cell(0, 10, truncated)
                except Exception as e2:
                    print(f"Failed again with truncated line: {e2}")
                    # Skip line if still failing

    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer.read()
