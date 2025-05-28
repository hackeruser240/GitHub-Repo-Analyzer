import requests
import os
import json
import matplotlib.pyplot as plt
import argparse as ag

from scripts.variables import var
from scripts.contributors import (
    lowest_contributors,
    lowest_contributors_VIZ,
    top_contributors_VIZ,
    top_contributors
)
from scripts.commits import extracting_authors
from scripts.savetoPDF import save_to_PDF
from scripts.helperFunctions import make_repo_folder


#headers = {'Authorization': f'token {var.token}'}


def contributors(repo,viz=False):

    if not repo.startswith('https://api.github.com/repos/'):
        print(f"Finding the contributors of {repo} repo")
        contributors = f'https://api.github.com/repos/{repo}/contributors?per_page=50'
    else:
        f=repo.split("/")
        repo=f[4]+'/'+f[5]
        print(f"Finding the contributors of repo: {repo}")
        contributors = f'https://api.github.com/repos/{repo}/contributors?per_page=50'
    
    response = requests.get(contributors, headers=var.headers)
    
    if response.status_code == 200:
        data = response.json()

        try:
            #path= os.path.join(make_repo_folder(), 'Data')
            path=make_repo_folder()
            os.makedirs(path,exist_ok=True)

            filepath=os.path.join(path,'contributions.json')

            with open(filepath,'w') as file:
                json.dump(data, file, indent=4 )

                print("✅ Saved contributions.json")
        except:
            print('❌ Failed to save contributions.json')
        
        print(f"✅ Successfully fetched { len(data) } users in the JSON file")
        
        print("***** Contribution of each user *****")
        for i,contributor in enumerate(data,start=1):
            print(f"{i}.", contributor['login'],':', contributor['contributions'])

        print("***** Searching for Bots *****")
        for user in data:
            if user['type'] != 'User':
                print(user['login'])
        
        #Printing data:

        top_contributors(data)
        if viz:
            top_contributors_VIZ(data)
        
        lowest_contributors(data)
        if viz:
            lowest_contributors_VIZ(data)

    else:
        print(f"❌ Failed to fetch data. Status Code: {response.status_code}")
        print("Reason:", response.json().get("message", "Unknown error"))

def commits(var):
    
    print(f"Finding latest commits of {var.repo} repo")

    commits= f'https://api.github.com/repos/{var.repo}/commits?per_page=50'
    response = requests.get(commits, headers=var.headers)
    
    if response.status_code==200:
        data=response.json()
        print(f"Total {len(data)} commits found")
        try:
            #path=r'Data'
            os.makedirs(var.path,exist_ok=True)
            filepath=os.path.join(var.path,'commits.json')
            
            var.save_dir=filepath
            
            with open(filepath,'w') as file:
                json.dump(data, file, indent=4 )
                print("✅ Saved commits.json")
        except:
            print('❌ Failed to save commits.json')

        try:
            extracting_authors(filepath,commit_author_viz=True)
        except Exception as e:
            print(f"Couldn't process extracting_authors() as per error: \n {e}")
    else:
        print(f"❌ Failed to fetch data. Status Code: {response.status_code}")
        print("Reason:", response.json().get("message", "Unknown error"))

if __name__=="__main__":
    parser=ag.ArgumentParser()
    parser.add_argument('--repo', required=True, help="Repo in the form 'owner/name' or full API URL")
    args=parser.parse_args()
    var.repo=args.repo

    contributors(args.repo)
    #commits(var)
    save_to_PDF(var)