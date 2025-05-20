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


headers = {'Authorization': f'token {var.token}'}

# Example repo: facebook/react
#repo = 'facebook/react'

def contributors(repo,viz=False):

    if not repo.startswith('https://api.github.com/repos/'):
        print(f"Finding the contributors of {repo} repo")
        contributors = f'https://api.github.com/repos/{repo}/contributors'
    else:
        f=repo.split("/")
        repo=f[4]+'/'+f[5]
        print(f"Finding the contributors of repo: {repo}")
        contributors = f'https://api.github.com/repos/{repo}/contributors'
    
    response = requests.get(contributors, headers=headers)
    
    if response.status_code == 200:
        data = response.json()

        with open('contributions.json','w') as file:
            json.dump( data, file, indent=4 )
        
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

def commits(repo,viz=False):
    
    print(f"Finding latest commtis of {repo} repo")

    commits= f'https://api.github.com/repos/{repo}/commits'
    response = requests.get(commits, headers=headers)
    
    if response.status_code==200:
        data=response.json()

        try:
            with open('commits.json','w') as file:
                json.dump(data, file, indent=4 )
        except:
            print('Failed to save commits.json')
    else:
        print(f"❌ Failed to fetch data. Status Code: {response.status_code}")
        print("Reason:", response.json().get("message", "Unknown error"))

if __name__=="__main__":
    parser=ag.ArgumentParser()
    parser.add_argument('--repo',required=True,help="Repo in the form 'owner/name' or full API URL")
    args=parser.parse_args()
    
    var.repo=args.repo
    
    contributors(var.repo,viz=True)