import json
import matplotlib.pyplot as plt
import numpy as np
import sys,os
# Add parent directory (project root) to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tabulate import tabulate #used in commit_title_visualization()

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from scripts.variables import var

def loading_json_file(filename):

    #filename=r'C:\Users\HP\OneDrive\Documents\GithubRepos\Data\commits.json'
    if os.path.isfile(filename) and filename.lower().endswith('.json') :
        print(f" '{filename}' is a valid path! ")
        with open(filename,'r') as f:
            commits=json.load(f)
        print('Length of commit.json :',len(commits))
        return commits
    else:
        print("Location: commits.py -> loading_json_file()")
        print(f" Please correct '{filename}' path")
        
def printing_commit_authors():
    var.authors=dict(sorted(var.authors.items(), key=lambda item: item[1], reverse=True) )
    
    print(f"Authors in order of greatest commits:")
    for key,value in var.authors.items():
        print(f"{key}:{value} commits")

def commit_author_visualization():

    # Sort and prepare data
    sorted_authors = sorted(var.authors.items(), key=lambda x: x[1], reverse=True)
    names, counts = zip(*sorted_authors)

    # Optional: scale counts to reduce visual dominance
    # Option A: Square root scaling
    scaled_counts = [np.sqrt(c) for c in counts]

    # Option B: Log scale
    # scaled_counts = [np.log(c+1) for c in counts]

    # Plot
    plt.figure(figsize=(10, 6))
    bars = plt.barh(names, scaled_counts, color='skyblue')
    plt.xlabel('Scaled Contribution (√count)')
    plt.title('Author Contributions (Scaled View)')
    plt.gca().invert_yaxis()  # Highest contributor on top

    # Add labels
    for bar, count in zip(bars, counts):
        plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                f"{count} commits", va='center')

    plt.tight_layout()
    
    try: 
        path=r'Data\Images'
        os.makedirs(path,exist_ok=True)

        filepath=os.path.join( path, "Authors by Commit Timeline.png")
        plt.savefig(filepath,dpi=300)
        print("✅ Saved: Authors by Commit Timeline.png")
    except:
        print("❌Failed to save the authors by timeline image")

def commit_title_visualization(commits,filename):
    
    clean_messages = []

    for commit in commits:
        commit_data = commit.get('commit')
        if commit_data:
            message = commit_data.get('message', '')
            title = message.split('\n\n')[0].strip()
            clean_messages.append(title)
            

    try:
        table = [(i + 1, msg) for i, msg in enumerate(clean_messages)]
        print("Title of latest commits:")
        print(tabulate(table, headers=["#", "Commit Title"], tablefmt="fancy_grid"))
    except:
        print("Title of latest commits could NOT be populated")


    try:
        #filepath=os.path.dirname(filename)
        #print(f"filename:{filename}")
        save_to_PDF(clean_messages,filename)
    except Exception as e:
        print("Error in commits.py -> extracting_authors() -> commit_title_visualization() -> save_to_PDF()")
        print(f"Error: {e}")

def save_to_PDF(commit_titles, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    save_path=os.path.join( os.path.dirname(save_path) ,"Commit Titles.pdf")

    c = canvas.Canvas(save_path, pagesize=letter)
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

    for i, msg in enumerate(commit_titles, start=1):
        text = f"{i}. {msg}"
        c.drawString(1 * inch, y, text)
        y -= 0.25 * inch  # adjust spacing

        if y < 1 * inch:
            c.showPage()  # new page
            y = height - 1 * inch
            c.setFont("Helvetica", 10)

    c.save()
    
    print(f"PDF saved at: {save_path}")

def extracting_authors(filename,viz=False):
    commits=loading_json_file(filename)
    #authors={}
    raw_author=[]
    if commits:
        #print("Extracting author logins:")
        for commit_dict in commits: 
            author = commit_dict.get('author')
            if author and isinstance(author, dict):
                
                login = author.get('login') # Use .get() here too for safety
                raw_author.append(login)

                if login not in var.authors: 
                    var.authors[login] = 1
                else:
                    var.authors[login] += 1
            else:
                print("Warning: 'author' key missing or not a dictionary for a commit.")
        
        
        try:
            #Printing the author dictionary
            printing_commit_authors()
        except:
            print("Some error in commits.py -> printing_commit_authors()")


        print("Authors in order of timeline:")
        for num,item in enumerate(raw_author[:6],start=1) :
            print(f"{num}. {item}")


        try:
            if viz:
                commit_author_visualization()
        except:
            print("Some error in commits.py -> commit_author_visualization() ")

        
        try:
            if viz:
                commit_title_visualization(commits,filename)
        except:
            print("Some error in commits.py -> commit_title_visualization() ")
    
    else:
        print("No commit data loaded to process.")

if __name__=='__main__':
    filepath=r'C:\Users\HP\OneDrive\Documents\GithubRepos\Data'
    filename=r'C:\Users\HP\OneDrive\Documents\GithubRepos\Data\commits.json'

    extracting_authors(filename,viz=True)