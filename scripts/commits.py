import json
from scripts.variables import var

def loading_json_file(filename):

    #filename=r'C:\Users\HP\OneDrive\Documents\GithubRepos\Data\commits.json'

    with open(filename,'r') as f:
        commits=json.load(f)
    print('Length of commit:',len(commits))
    return commits


def extracting_authors(filename):
    commits=loading_json_file(filename)
    #authors={}
    if commits:
        print("Extracting author logins:")
        for commit_dict in commits: 
            author = commit_dict.get('author')
            if author and isinstance(author, dict):
                login = author.get('login') # Use .get() here too for safety
                if login not in var.authors: 
                    var.authors[login] = 1
                else:
                    var.authors[login] += 1
            else:
                print("Warning: 'author' key missing or not a dictionary for a commit.")
    else:
        print("No commit data loaded to process.")

if __name__=='__main__':
    filename=r'C:\Users\HP\OneDrive\Documents\GithubRepos\Data\commits.json'

    extracting_authors(filename)
    print(f"Authors: {var.authors}")