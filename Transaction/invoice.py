from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
import datetime

def generate_invoice(data, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 50, "INVOICE")

    c.setStrokeColor(colors.grey)
    c.setLineWidth(1)
    c.rect(30, height - 279, width - 80, 200, stroke=1, fill=0)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, height - 100, "User:")
    c.setFont("Helvetica", 12)
    c.drawString(155, height - 100, data["user"])

    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, height - 120, "Email:")
    c.setFont("Helvetica", 12)
    c.drawString(155, height - 120, data["email"])

    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, height - 160, "Stock:")
    c.setFont("Helvetica", 12)
    c.drawString(155, height - 160, data["stock"])

    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, height - 180, "Quantity:")
    c.setFont("Helvetica", 12)
    c.drawString(155, height - 180, str(data["quantity"]))

    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, height - 200, "Price per Share:")
    c.setFont("Helvetica", 12)
    c.drawString(155, height - 200, f" {data['price']}")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, height - 220, "Total:")
    c.setFont("Helvetica", 12)
    c.drawString(155, height - 220, f" {data['quantity'] * data['price']}")

    now = datetime.datetime.now()
    formatted_date = now.strftime("%d-%m-%Y")  
    formatted_time = now.strftime("%I:%M %p")  

    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, height - 240, "Date:")
    c.setFont("Helvetica", 12)
    c.drawString(158, height - 240, formatted_date)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, height - 260, "Time:")
    c.setFont("Helvetica", 12)
    c.drawString(158, height - 260, formatted_time)

    # Footer line
    c.setStrokeColor(colors.black)
    c.line(40, 50, width - 40, 50)
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(width / 2, 35, "Thank you for your purchase!")

    c.save()


# import os
# from fastapi import APIRouter, Depends, HTTPException
# from fastapi.responses import FileResponse
# from sqlalchemy.orm import Session
# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_CENTER, TA_RIGHT
# from reportlab.lib import colors
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase.pdfmetrics import registerFontFamily
# from datetime import datetime

# pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
# pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))
# registerFontFamily('Arial', normal='Arial', bold='Arial-Bold')

# def format_inr(amount):
#     return f"₹ {amount:,.0f}"

# def generate_invoice(data, file_path):
#     doc = SimpleDocTemplate(file_path, pagesize=A4)
#     styles = getSampleStyleSheet()

#     title_style = ParagraphStyle(
#         'TitleStyle',
#         parent=styles['Title'],
#         fontName='Arial-Bold',
#         fontSize=22,
#         alignment=TA_CENTER,
#         textColor=colors.darkblue,
#         spaceAfter=20
#     )

#     header_style = ParagraphStyle(
#         'HeaderStyle',
#         parent=styles['Heading2'],
#         fontName='Arial-Bold',
#         fontSize=14,
#         textColor=colors.black,
#         spaceAfter=5
#     )

#     normal_style = ParagraphStyle(
#         'NormalStyle',
#         parent=styles['Normal'],
#         fontName='Arial',
#         fontSize=12,
#         textColor=colors.black
#     )

#     story = []
#     story.append(Paragraph("INVOICE", title_style))
#     story.append(Spacer(1, 20))


#     story.append(Paragraph(f"Customer: {data['user']}", header_style))
#     story.append(Spacer(1, 7))
#     story.append(Paragraph(f"Email: {data['email']}", normal_style))
#     story.append(Spacer(1, 7))
#     story.append(Paragraph(f"Date: {data['Date'].strftime('%d-%m-%Y')}", normal_style))
#     story.append(Spacer(1, 7))
#     story.append(Paragraph(f"Time: {data['Date'].strftime('%I:%M:%S %p')}", normal_style))

#     story.append(Spacer(1, 15))



#     total = data["quantity"] * data["price"]
#     table_data = [
#         ["Item", "Qty", "Price", "Total"],
#         [data["stock"], str(data["quantity"]), format_inr(data["price"]), format_inr(total)],
#         ["", "", "Grand Total", format_inr(total)]
#     ]

#     table = Table(table_data, colWidths=[150, 60, 100, 100])
#     table.setStyle(TableStyle([
#         ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
#         ('FONTSIZE', (0, 0), (-1, -1), 12),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
#         ('ALIGN', (0, 0), (-1, 0), 'CENTER'), 
#         ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
#         ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'),
#         ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
#         ('BACKGROUND', (0, 1), (-1, -2), colors.whitesmoke),
#         ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
#         ('FONTNAME', (0, -1), (-1, -1), 'Arial-Bold'),  
#     ]))

#     story.append(table)
#     story.append(Spacer(1, 30))
#     story.append(Paragraph("Thank you for your purchase!", normal_style))

#     doc.build(story)
    