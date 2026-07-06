"""IEEE-styled PDF export via ReportLab. Returns bytes for st.download_button."""
from __future__ import annotations

from io import BytesIO

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

_ROMAN = {
    "Introduction": "I", "Methodology": "II", "Implementation": "III",
    "Results": "IV", "Conclusion": "V",
}

TITLE = ParagraphStyle("Title", fontName="Times-Bold", fontSize=18, leading=22,
                       alignment=TA_CENTER, spaceAfter=6)
AUTHOR = ParagraphStyle("Author", fontName="Times-Roman", fontSize=11, leading=14,
                        alignment=TA_CENTER, spaceAfter=2)
HEADING = ParagraphStyle("Heading", fontName="Times-Bold", fontSize=12, leading=15,
                         spaceBefore=12, spaceAfter=5)
BODY = ParagraphStyle("Body", fontName="Times-Roman", fontSize=10.5, leading=13.5,
                      alignment=TA_JUSTIFY, spaceAfter=7, firstLineIndent=14)
ABSTRACT = ParagraphStyle("Abstract", parent=BODY, fontName="Times-Italic",
                          firstLineIndent=0)
REF = ParagraphStyle("Ref", parent=BODY, fontSize=9.5, leading=12,
                     firstLineIndent=0, leftIndent=14, spaceAfter=3)


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_pdf(title: str, author: str, institution: str, sections: dict[str, str]) -> bytes:
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        leftMargin=0.85 * inch, rightMargin=0.85 * inch,
        topMargin=0.85 * inch, bottomMargin=0.85 * inch,
        title=title, author=author,
    )

    story = [
        Paragraph(_escape(title), TITLE),
        Paragraph(_escape(author), AUTHOR),
        Paragraph(_escape(institution), AUTHOR),
        Spacer(1, 14),
    ]

    if "Abstract" in sections:
        text = _escape(sections["Abstract"].strip())
        story.append(Paragraph(f"<b>Abstract—</b>{text}", ABSTRACT))
        story.append(Spacer(1, 6))

    for name in ("Introduction", "Methodology", "Implementation", "Results", "Conclusion"):
        if name not in sections:
            continue
        story.append(Paragraph(f"{_ROMAN[name]}. {name.upper()}", HEADING))
        for para in sections[name].split("\n\n"):
            if para.strip():
                story.append(Paragraph(_escape(para.strip()), BODY))

    if "References" in sections:
        story.append(Paragraph("REFERENCES", HEADING))
        for line in sections["References"].splitlines():
            if line.strip():
                story.append(Paragraph(_escape(line.strip()), REF))

    doc.build(story)
    return buf.getvalue()
