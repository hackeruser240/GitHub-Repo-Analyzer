import sys,os

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def save_to_PDF(var):
    os.makedirs(os.path.dirname(var.save_dir), exist_ok=True)
    var.save_dir=os.path.join( os.path.dirname(var.save_dir) ,"Commit Titles.pdf")

    c = canvas.Canvas(var.save_dir, pagesize=letter)
    width, height = letter
    
    maintitle=f"'{var.repo}' details"
    c.setFont("Helvetica-Bold", 16)
    main_title_width = c.stringWidth(maintitle, "Helvetica-Bold", 16)
    c.drawString((width - main_title_width) / 2, height - 1 * inch, maintitle)

    sub_title = "Commit Titles:"
    c.setFont("Helvetica-Bold", 14)
    c.stringWidth(sub_title, "Helvetica-Bold", 14)
    #sub_title_width = c.stringWidth(sub_title, "Helvetica", 14)
    c.drawString(1*inch, height - 1.3 * inch, sub_title)

    c.setFont("Helvetica", 10)
    y = height - 1.6 * inch

    for i, msg in enumerate(var.commit_titles, start=1):
        text = f"{i}. {msg}"
        c.drawString(1 * inch, y, text)
        y -= 0.25 * inch  # adjust spacing

        if y < 1 * inch:
            c.showPage()  # new page
            y = height - 1 * inch
            c.setFont("Helvetica", 10)

    c.save()
    
    print(f"PDF saved at: {var.save_dir}")