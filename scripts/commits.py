import json
import matplotlib.pyplot as plt
import numpy as np
import sys,os
# Add parent directory (project root) to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tabulate import tabulate #used in commit_title_visualization()

from scripts.variables import var
from scripts.savetoPDF import save_to_PDF

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

    print("Authors in order of timeline:")
    for num,item in enumerate(var.raw_authors[:6],start=1) :
        print(f"{num}. {item}")

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

def commit_title_visualization(commits,commit_title_viz=False):

    for commit in commits:
        commit_data = commit.get('commit')
        if commit_data:
            message = commit_data.get('message', '')
            title = message.split('\n\n')[0].strip()
            var.commit_titles.append(title)

    
    if commit_title_viz:
        try:
            table = [(i + 1, msg) for i, msg in enumerate(var.commit_titles)]
            print("Title of latest commits:")
            print(tabulate(table, headers=["#", "Commit Title"], tablefmt="fancy_grid"))
        except:
            print("Title of latest commits could NOT be populated")



#===============================================================================================
#===========================================main.py()===========================================
#===============================================================================================

def extracting_authors(filename,commit_author_viz=False,commit_title_viz=False):
    commits=loading_json_file(filename)
    
    if commits:
        #print("Extracting author logins:")
        for commit_dict in commits: 
            author = commit_dict.get('author')
            if author and isinstance(author, dict):
                
                login = author.get('login') # Use .get() here too for safety
                var.raw_authors.append(login)

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


        try:
            if commit_author_viz:
                commit_author_visualization()
        except:
            print("Some error in commits.py -> commit_author_visualization()")

        
        try:
            commit_title_visualization(commits,commit_title_viz=False)
        except Exception as e:
            print("Some error in commits.py -> commit_title_visualization()")
            print(f"Error: {e}")
    
    else:
        print("No commit data loaded to process.")

if __name__=='__main__':
    
    import requests
    from scripts.variables import var
    
    filename=r'C:\Users\HP\OneDrive\Documents\GithubRepos\Data\commits.json'
    headers = {'Authorization': f'token {var.token}'}
    
    print(f"Finding latest commits of {var.repo} repo")

    commits= f'https://api.github.com/repos/{var.repo}/commits'
    response = requests.get(commits, headers=headers)
    
    if response.status_code==200:
        data=response.json()
        print(f"Total {len(data)} commits found")
        try:
            path=r'Data'
            os.makedirs(path,exist_ok=True)
            filepath=os.path.join(path,'commits.json')
            with open(filepath,'w') as file:
                json.dump(data, file, indent=4 )
                print("✅ Saved commits.json")
        except:
            print('❌ Failed to save commits.json')

    extracting_authors(filename,viz=True)