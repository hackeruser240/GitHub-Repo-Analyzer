import requests
import os
import pandas as pd
import json
import matplotlib.pyplot as plt
import argparse as ag

from scripts.variables import Variables

var=Variables()

headers = {'Authorization': f'token {var.token}'}

# Example repo: facebook/react
#repo = 'facebook/react'


def lowest_contributors(data,n=100):
    '''
    finding the lowest contributors with contributions<n.
    by default n=10
    '''

    print(f"*****Finding lowest {n} contributors in '{args.repo}'*****")
    #low=sorted(data, key=lambda x:x['contributions'],reverse=False)
    
    lowest=[user for user in data if user['contributions']<n]

    print(f"Users with ≤{n} contributions: {len(lowest)}")
    x,y=[],[]
    for user in lowest:
        if user['type'] == 'User':
            print(f"{user['login']} - {user['contributions']}")
            x.append(user['login'])
            y.append(user['contributions'])
        
        elif user['type'] == 'bot' or 'Bot':
            #print('Bot detected! Ignoring!')
            pass

def lowest_contributors_VIZ(data, n=100):            
    
    lowest=[user for user in data if user['contributions']<n]

    print(f"Users with ≤{n} contributions: {len(lowest)}")
    x,y=[],[]
    for user in lowest:
        if user['type'] == 'User':
            print(f"{user['login']} - {user['contributions']}")
            x.append(user['login'])
            y.append(user['contributions'])
        
        elif user['type'] == 'bot' or 'Bot':
            print('Bot detected! Ignoring!')

    offset=0.5
    plt.figure(figsize=(10, 6))  # Width x Height in inches
    for i, (xi, yi) in enumerate(zip(x, y)):
        plt.text(xi, yi+offset, str(yi), ha='center', va='bottom', fontsize=9)
    plt.plot(x, y, marker='o', linestyle='-', color='tab:blue')
    plt.title(f"Least {n} Contributions", fontsize=16)
    plt.xlabel("Username", fontsize=12)
    plt.ylabel("# of Contributions", fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    #plt.legend(loc='best')
    plt.tight_layout()
    plt.show()

def top_contributors_VIZ(data,n=10):
    '''
    Gets the top n contributors and visualizes them
    '''
    
    print(f"*****Visualizing top {n} contributors in '{args.repo}'*****")

    # Get top 10 contributors
    top=top_contributors(data)
    top=top[:n]

    names = [user['login'] for user in top]
    contribs = [user['contributions'] for user in top]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(names, contribs, color='skyblue')

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,  # X: center of bar
            height,                             # Y: top of bar
            str(height),                        # Label text
            ha='center', va='bottom'            # Align center/bottom
        )

    plt.title("Top 10 Contributors")
    plt.xlabel("Username")
    plt.ylabel("Contributions")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def top_contributors(data,n=10):
    '''
    Using the response, printing the most contributors, 5 by default
    '''
    print(f"*****Finding top {n} contributors in '{args.repo}'*****")
    top_contributors = sorted(data, key=lambda x: x['contributions'], reverse=True)

    for i, user in enumerate(top_contributors[:n], start=1):
        print(f"{i}. {user['login']} - {user['contributions']} contributions")

    return top_contributors

def contributors(repo,viz=False):

    if not repo.startswith('https://api.github.com/repos/'):
        print(f"Finding the contributors of {repo} repo")
        contributors = f'https://api.github.com/repos/{repo}/contributors'
        print(contributors)
    else:
        f=repo.split("/")
        repo=f[4]+'/'+f[5]
        print(f"Finding the contributors of repo: {repo}")
        contributors = f'https://api.github.com/repos/{repo}/contributors'
    
    response = requests.get(contributors, headers=headers)
    
    if response.status_code == 200:
        data = response.json()

        with open('data.json','w') as file:
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
        if not viz:
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
        #print(data)

        try:
            with open('commits.json','w') as file:
                json.dump(data, file, indent=4 )
        except:
            print('Failed to save commits.json')
    else:
        print("Commit website not gotten.")

if __name__=="__main__":
    parser=ag.ArgumentParser()
    parser.add_argument('--repo',required=True,help="Repo in the form 'owner/name' or full API URL")
    args=parser.parse_args()
    
    contributors(args.repo,viz=True)