import requests
import os
import json
import matplotlib.pyplot as plt
import argparse as ag

from scripts.variables import var
from scripts.contributors import (
    user_contributions,
    lowest_contributors,
    lowest_contributors_VIZ,
    top_contributors_VIZ,
    top_contributors
)
from scripts.commits import processing_commits
from scripts.savetoPDF import save_to_PDF
from scripts.helperFunctions import (
    make_repo_folder,
    suppress_stdout,
    Logger
)


#headers = {'Authorization': f'token {var.token}'}


def contributors(repo,log,inline_display=False,viz=True):

    if not repo.startswith('https://api.github.com/repos/'):
        print("\n*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=")
        print(f"Finding the contributors of {repo} repo")
        print("*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=")
        contributors = f'https://api.github.com/repos/{repo}/contributors?per_page=50'
    else:
        f=repo.split("/")
        repo=f[4]+'/'+f[5]
        print("*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=")
        print(f"Finding the contributors of repo: {repo}")
        print("*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=")
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

                print(f"✅ Saved: {len(data)} users in contributions.json")
        except:
            print('❌ Failed to save contributions.json')
        
        #print(f"✅ Successfully fetched { len(data) } users in the JSON file")
        
        with suppress_stdout(enabled=inline_display):
            user_contributions(data)
        
        #print(f"Error in main.py -> user_contributions()\n{e}")

        def bots():
            print("***** Searching for Bots *****")
            for user in data:
                if user['type'] != 'User':
                    print(user['login'])
        
        #Printing data:
        with suppress_stdout(enabled=inline_display):
                top_contributors(data,log)
        try:           
            if viz:
                top_contributors_VIZ(data)
        except Exception as e:
            print(f"Error in main.py -> contributors() -> Finding top contributors\n{e}")
        
        with suppress_stdout(enabled=inline_display):
                lowest_contributors(data)

        try:
            if viz:
                lowest_contributors_VIZ(data)
        except Exception as e:
            print(f"Error in main.py -> contributors() -> Finding lowest contributors\n{e}")

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
            os.makedirs(make_repo_folder(),exist_ok=True)
            filepath=os.path.join(make_repo_folder(),'commits.json')
            
            var.save_dir=filepath
            
            with open(filepath,'w') as file:
                json.dump(data, file, indent=4 )
                print("✅ Saved commits.json")
        except:
            print('❌ Failed to save commits.json')

        try:
            processing_commits(filepath,author_inline=False)
        except Exception as e:
            print(f"Couldn't process extracting_authors() as per error: \n {e}")
    else:
        print(f"❌ Failed to fetch data. Status Code: {response.status_code}")
        print("Reason:", response.json().get("message", "Unknown error"))

if __name__=="__main__":
    log=Logger(use_streamlit=False)
    parser=ag.ArgumentParser()
    parser.add_argument('--repo', required=True, help="Repo in the form 'owner/name' or full API URL")
    args=parser.parse_args()
    var.repo=args.repo

    contributors(args.repo,log=log,inline_display=True)
    commits(var)
    print("=====================================")
    save_to_PDF(var)
    print("=====================================")