import matplotlib.pyplot as plt

from scripts.variables import var
from scripts.helperFunctions import save_fig


def user_contributions(data):
    print("=========================")
    print("Contribution of each user")
    print("=========================")
    for i,contributor in enumerate(data,start=1):
        print(f"{i}.", contributor['login'],':', contributor['contributions'])

def lowest_contributors(data,n=var.numof_lowest_contributions):
    '''
    finding the lowest contributors with contributions<n.
    by default n=100
    '''

    print("==================================================")
    print(f"Finding lowest {n} contributors in '{var.repo}'")
    print("==================================================")
    #low=sorted(data, key=lambda x:x['contributions'],reverse=False)
    
    var.lowest_contribution=[user for user in data if user['contributions']<n]

    print(f"Users with ≤{n} contributions: {len(var.lowest_contribution)}")
    x,y=[],[]
    for user in var.lowest_contribution:
        if user['type'] == 'User':
            print(f"{user['login']} - {user['contributions']}")
            x.append(user['login'])
            y.append(user['contributions'])
        
        elif user['type'] == 'bot' or 'Bot':
            #print('Bot detected! Ignoring!')
            pass

    return var.lowest_contribution

def lowest_contributors_VIZ(data, n=var.numof_lowest_contributions):            
    
    lowest=[user for user in data if user['contributions']<n]

    #print(f"Users with ≤{n} contributions: {len(lowest)}")
    x,y=[],[]
    for user in lowest:
        if user['type'] == 'User':
            x.append(user['login'])
            y.append(user['contributions'])
        
        elif user['type'] == 'bot' or 'Bot':
            #print('Bot detected! Ignoring!')
            pass

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
        save_fig(name='Least contributors.png')
        print("✅ Saved: 'Least contributors.png' ")
    except:
        print("❌Failed to save the lowest contributors image")

def top_contributors(data,log,n=var.numof_top_contributors):
    '''
    Using the response, printing the most contributors, 5 by default
    '''
    log("=================================================")
    log(f"Finding top {n} contributors in '{var.repo}'")
    log("=================================================")
    var.top_contributors = sorted(data, key=lambda x: x['contributions'], reverse=True)

    for i, user in enumerate(var.top_contributors[:n], start=1):
        log(f"{i}. {user['login']} - {user['contributions']} contributions")

def top_contributors_VIZ(data,n=var.numof_top_contributors):
    '''
    Gets the top n contributors and visualizes them
    '''
    
    #print(f"*****Visualizing top {n} contributors in '{var.repo}'*****")

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
        save_fig(name="Top 10 contributors.png")
        print(f"✅ Saved: 'Top {n} contributors.png'")
    except Exception as e:
        print(f"❌Failed to save the highest contributors image. Error:\n{e}")
