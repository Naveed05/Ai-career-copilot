from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def build_pdf(analysis: dict, interview_questions: list[dict], cover_letter: str = "") -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=42)
    styles = getSampleStyleSheet()
    title = ParagraphStyle("Title", parent=styles["Title"], alignment=TA_CENTER, spaceAfter=12)
    heading = ParagraphStyle("Heading", parent=styles["Heading2"], spaceBefore=10, spaceAfter=6)
    body = styles["BodyText"]
    story = [Paragraph("AI Career Copilot — Career Report", title)]

    score = analysis.get("match_score", 0)
    data = [
        ["ATS-style match", f"{score}%"],
        ["Strengths", str(len(analysis.get("strengths", [])))],
        ["Skill gaps", str(len(analysis.get("skill_gaps", [])))],
    ]
    table = Table(data, colWidths=[180, 100])
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
        ("PADDING", (0, 0), (-1, -1), 7),
    ]))
    story += [table, Spacer(1, 12)]

    sections = [
        ("Summary", [analysis.get("summary", "")]),
        ("Strengths", analysis.get("strengths", [])),
        ("Skill gaps", analysis.get("skill_gaps", [])),
        ("Recommendations", analysis.get("recommendations", [])),
    ]
    for heading_text, items in sections:
        story.append(Paragraph(heading_text, heading))
        for item in items:
            story.append(Paragraph(f"• {item}", body))
            story.append(Spacer(1, 3))

    if interview_questions:
        story.append(Paragraph("Interview Coach", heading))
        for item in interview_questions:
            story.append(Paragraph(f"<b>{item.get('category', 'Question')}:</b> {item.get('question', '')}", body))
            story.append(Spacer(1, 4))

    if cover_letter:
        story.append(Paragraph("Cover Letter", heading))
        for paragraph in cover_letter.split("\n\n"):
            story.append(Paragraph(paragraph.replace("\n", "<br/>"), body))
            story.append(Spacer(1, 5))

    doc.build(story)
    return buffer.getvalue()
