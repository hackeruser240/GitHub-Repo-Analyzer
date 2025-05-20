import argparse
import matplotlib.pyplot as plt
import os

from scripts.variables import var


def lowest_contributors(data,n=var.lowest_contributions):
    '''
    finding the lowest contributors with contributions<n.
    by default n=100
    '''

    print(f"*****Finding lowest {n} contributors in '{var.repo}'*****")
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

    return lowest

def lowest_contributors_VIZ(data, n=var.lowest_contributions):            
    
    lowest=[user for user in data if user['contributions']<n]

    print(f"Users with ≤{n} contributions: {len(lowest)}")
    x,y=[],[]
    for user in lowest:
        if user['type'] == 'User':
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

    try: 
        path=r'Data\Images'
        os.makedirs(path,exist_ok=True)

        filepath=os.path.join( path, "Least contributors.png")
        plt.savefig(filepath,dpi=300) 
        print("✅ Saved Least contributors.png")
    except:
        print("❌Failed to save the lowest contributors image")

def top_contributors(data,n=var.top_contributors):
    '''
    Using the response, printing the most contributors, 5 by default
    '''
    print(f"*****Finding top {n} contributors in '{var.repo}'*****")
    top_contributors = sorted(data, key=lambda x: x['contributions'], reverse=True)

    for i, user in enumerate(top_contributors[:n], start=1):
        print(f"{i}. {user['login']} - {user['contributions']} contributions")

def top_contributors_VIZ(data,n=var.top_contributors):
    '''
    Gets the top n contributors and visualizes them
    '''
    
    print(f"*****Visualizing top {n} contributors in '{var.repo}'*****")

    # Get top 10 contributors
    top=sorted(data, key=lambda x: x['contributions'], reverse=True)[:n]

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

    try: 
        path=r'Data\Images'
        os.makedirs(path,exist_ok=True)

        filepath=os.path.join( path, "Top 10 contributors.png")
        plt.savefig(filepath,dpi=300)
        print("✅ Top 10 contributors.png")
    except:
        print("❌Failed to save the highest contributors image")