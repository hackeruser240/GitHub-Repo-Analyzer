import os

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def title(var):
    maintitle=f"'{var.repo}' details"
    var.c.setFont("Helvetica-Bold", var.f1_font)
    main_title_width = var.c.stringWidth(maintitle, "Helvetica-Bold", var.f1_font)
    var.c.drawString((var.width - main_title_width) / 2, var.y, maintitle)
    var.y -= 0.3*inch

def commit_titles(var):
    if var.commit_titles==[]:
        pass
    else:
        sub_title = "Commit Titles:"
        var.c.setFont("Helvetica-Bold", var.f2_font)
        var.c.stringWidth(sub_title, "Helvetica-Bold", var.f2_font)
        var.c.drawString(1*inch, var.height - 1.3 * inch, sub_title)

        var.c.setFont("Helvetica", var.f3_font)
        var.y -= 0.2 * inch

        for i, msg in enumerate(var.commit_titles, start=1):
            text = f"{i}. {msg}"
            var.c.drawString(1 * inch, var.y, text)
            var.y -= 0.25 * inch  # adjust spacing

            if var.y < 1 * inch:
                var.c.showPage()  # new page
                var.y = var.height - 1 * inch
            var.c.setFont("Helvetica", var.f3_font)

def commit_authorsNcounts(var):
    if var.raw_authors==[]:
        pass
    else:
        # Set up font
        var.c.setFont("Helvetica-Bold", var.f2_font)
        var.y -= 0.3 * inch
        var.c.drawString(1 * inch, var.y, "Commit authors in order of greatest commits:")

        # Switch to regular font
        var.c.setFont("Helvetica", var.f3_font)

        # Start below the heading
        #y = var.height - 1.3 * inch
        var.y -= 0.2 * inch

        # Sort authors before printing
        sorted_authors = sorted(var.authors.items(), key=lambda x: x[1], reverse=True)

        for i, (author, count) in enumerate(sorted_authors,start=1):
            line = f"{i}. {author}: {count} commits"
            var.c.drawString(1 * inch, var.y, line)
            var.y -= 0.2 * inch  # space between lines

            # Add new page if we run out of space
            if var.y < 1 * inch:
                var.c.showPage()
                var.y = var.height - 1 * inch
                var.c.setFont("Helvetica", var.f3_font)

def commit_raw_authors(var):
    if var.raw_authors==[]:
        pass
    else:
        # Add some vertical space before this section
        var.y -= 0.3 * inch

        var.c.setFont("Helvetica-Bold", 12)
        var.c.drawString(1 * inch, var.y, "Commit authors in order of timeline:")

        # Move cursor down
        var.y -= 0.2 * inch
        var.c.setFont("Helvetica", 10)

        # Print first 6 authors from var.raw_authors
        for num, item in enumerate(var.raw_authors[:6], start=1):
            line = f"{num}. {item}"
            var.c.drawString(1 * inch, var.y, line)
            var.y -= 0.2 * inch

            # Handle page overflow
            if var.y < 1 * inch:
                var.c.showPage()
                var.y = var.height - 1 * inch
                var.c.setFont("Helvetica", 10)

def top_contributors(var):
    if var.top_contributors==[]:
        pass
    else:
        # Add some vertical space before this section
        var.y -= 0.3 * inch

        var.c.setFont("Helvetica-Bold", 12)
        var.c.drawString(1 * inch, var.y, "List of top contributors:")

        # Move cursor down
        var.y -= 0.2 * inch
        var.c.setFont("Helvetica", 10)

        n=var.numof_top_contributors

        # Print first 6 authors from var.raw_authors
        for i, user in enumerate(var.top_contributors[:n], start=1):
            line = f"{i}. {user['login']} - {user['contributions']} contributions"
            var.c.drawString(1 * inch, var.y, line)
            var.y -= 0.2 * inch

            # Handle page overflow
            if var.y < 1 * inch:
                var.c.showPage()
                var.y = var.height - 1 * inch
                var.c.setFont("Helvetica", 10)

def save_to_PDF(var):
    os.makedirs(os.path.dirname(var.save_dir), exist_ok=True)
    var.save_dir=os.path.join( os.path.dirname(var.save_dir) ,"Commit Titles.pdf")
    var.c = canvas.Canvas(var.save_dir, pagesize=letter)
    var.width, var.height = letter
    var.y=var.height-1 * inch
    var.f1_font=14
    var.f2_font=12
    var.f3_font=10

    
    title(var)
    commit_titles(var)
    commit_authorsNcounts(var)
    commit_raw_authors(var)
    top_contributors(var)

    try:
        var.c.save()
        print(f"PDF saved at: {var.save_dir}")
    except PermissionError:
        print("⚠️ You forgot to close the PDF file!")

if __name__=='__main__':
    from variables import var
    var.save_dir=r'Data\LL' #Just a dummy address
    save_to_PDF(var)