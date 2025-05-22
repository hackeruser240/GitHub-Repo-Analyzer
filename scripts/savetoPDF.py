import os

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def title(var):
    maintitle=f"'{var.repo}' details"
    var.c.setFont("Helvetica-Bold", 16)
    main_title_width = var.c.stringWidth(maintitle, "Helvetica-Bold", 16)
    var.c.drawString((var.width - main_title_width) / 2, var.height - 1 * inch, maintitle)

def commit_titles(var):
    if var.commit_titles==[]:
        pass
    else:
        sub_title = "Commit Titles:"
        var.c.setFont("Helvetica-Bold", 14)
        var.c.stringWidth(sub_title, "Helvetica-Bold", 14)
        var.c.drawString(1*inch, var.height - 1.3 * inch, sub_title)

        var.c.setFont("Helvetica", 10)
        y = var.height - 1.6 * inch

        for i, msg in enumerate(var.commit_titles, start=1):
            text = f"{i}. {msg}"
            var.c.drawString(1 * inch, y, text)
            y -= 0.25 * inch  # adjust spacing

            if y < 1 * inch:
                var.c.showPage()  # new page
                y = var.height - 1 * inch
            var.c.setFont("Helvetica", 10)

def save_to_PDF(var):
    os.makedirs(os.path.dirname(var.save_dir), exist_ok=True)
    var.save_dir=os.path.join( os.path.dirname(var.save_dir) ,"Commit Titles.pdf")
    var.c = canvas.Canvas(var.save_dir, pagesize=letter)
    var.width, var.height = letter

    
    title(var)
    commit_titles(var)

    var.c.save()
    
    print(f"PDF saved at: {var.save_dir}")