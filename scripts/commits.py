import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys,os
# Add parent directory (project root) to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tabulate import tabulate #used in commit_title_visualization()
from wordcloud import WordCloud # used in commit_msg_wordcloud()

from scripts.variables import var
from scripts.helperFunctions import save_fig

def loading_json_file(filename):

    #filename=r'C:\Users\HP\OneDrive\Documents\GithubRepos\Data\commits.json'
    if os.path.isfile(filename) and filename.lower().endswith('.json') :
        #print(f"'{filename}' is a valid path! ")
        with open(filename,'r') as f:
            commits=json.load(f)
        print('Length of commit.json :',len(commits))
        return commits
    else:
        print("Location: commits.py -> loading_json_file()")
        print(f" Please correct '{filename}' path")
        
def printing_commit_authors():
    '''
    Printing the total commits per authors.
    With respect to greatest number of commits and time
    '''
    def authors_by_greatest_commits():
        print("=======================================")
        print(f"Authors in order of greatest commits:")
        print("=======================================")
        for key,value in var.authors.items():
            print(f"{key}:{value} commits")

    def authors_by_timeline():
        print("==============================")
        print("Authors in order of timeline:")
        print("==============================")
        for num,item in enumerate(var.raw_authors[:6],start=1) :
            print(f"{num}. {item}")
    
    var.authors=dict(sorted(var.authors.items(), key=lambda item: item[1], reverse=True) )

    authors_by_greatest_commits()
    authors_by_timeline()

def commit_author_visualization():
    plt.clf()  # Clear current figure
    plt.cla()

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
        save_fig(name="Authors by Commit Timeline.png")
    except:
        print("❌Failed to save the authors by timeline image")

def commit_title_visualization(commits,title_inline=False):

    for commit in commits:
        commit_data = commit.get('commit')
        if commit_data:
            message = commit_data.get('message', '')
            title = message.split('\n\n')[0].strip()
            var.commit_titles.append(title)

    
    if title_inline:
        try:
            table = [(i + 1, msg) for i, msg in enumerate(var.commit_titles)]
            print("Title of latest commits:")
            print(tabulate(table, headers=["#", "Commit Title"], tablefmt="fancy_grid"))
        except:
            print("Title of latest commits could NOT be populated")

def commits_per_day(commits):
    dates=[ commit.get('commit').get('author').get('date') for commit in commits]
    df=pd.DataFrame( { 'dates':pd.to_datetime(dates) } )
    df['Dates']=df['dates'].dt.date
    commit_counts=df.groupby("Dates").size()

    #Plotting:
    plt.clf()  # Clear current figure
    plt.cla()
    
    commit_counts.plot(kind='line', figsize=(12, 6), title="Commits/Day")
    plt.xlabel("Date")
    plt.ylabel("Number of Commits")
    plt.grid(True)
    plt.tight_layout()
    #plt.show()
    try: 
        save_fig(name="Commits per Day.png")
    except:
        print("❌Failed to save the Commits Per Day image")

def commits_perday_peruser(commits):
    # Extract author + commit date
    data = [
        {
            "author": commit.get('author', {}).get('login'),
            "date": commit.get('commit', {}).get('author', {}).get('date')
        }
        for commit in commits
        if commit.get('author') and commit.get('commit')
    ]

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date']).dt.date

    # Group by date and author
    freq = df.groupby(['date', 'author']).size().unstack(fill_value=0)

    plt.clf()  # Clear current figure
    plt.cla()

    # Plot
    freq.plot(kind='line', figsize=(14, 6), title='Commits/Day for Users')
    plt.xlabel("Date")
    plt.ylabel("Commits")
    plt.legend(title="User", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    #plt.show()

    try:
        save_fig(name="Commits per Day per User.png")
    except Exception as o:
        print(f"Error in commits.py -> commit_perday_peruser()! \n{o}")

def commit_msg_wordcloud(commits):
    # Extract commit messages
    messages = [
        commit.get('commit', {}).get('message', '')
        for commit in commits
        if commit.get('commit')
    ]

    # Join all messages into one string
    text = " ".join(messages).lower()

    # Optional: remove common irrelevant words
    common_stopwords = set(WordCloud().stopwords)
    more_stopwords = {"merge", "pull", "request", "from", "branch"}
    all_stopwords = common_stopwords.union(more_stopwords)

    # Generate word cloud
    wordcloud = WordCloud(
        width=1000,
        height=500,
        background_color='white',
        stopwords=all_stopwords,
        collocations=True
    ).generate(text)

    # Plot
    plt.clf()
    plt.cla()
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title("Common Terms in Commit Messages", fontsize=16)
    plt.tight_layout()
    #plt.show()

    try:
        save_fig(name="Wordcloud.png")
    except Exception as o:
        print(f"Error in commits.py -> commit_msg_wordcloud() \n{o}")


#===============================================================================================
#===========================================main.py()===========================================
#===============================================================================================

def processing_commits(filename,author_inline=True,author_plot=True,title_inline=False):
    
    try:
        commits=loading_json_file(filename)
    except Exception as d:
        print(f"Error in loading commits.json. Error: {d}")
    
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
            if author_inline:
                printing_commit_authors()
        except:
            print("Some error in commits.py -> printing_commit_authors()")


        try:
            if author_plot:
                commit_author_visualization()
        except:
            print("Some error in commits.py -> commit_author_visualization()")

        
        try:
            commit_title_visualization(commits,title_inline)
        except Exception as e:
            print("Some error in commits.py -> commit_title_visualization()")
            print(f"Error: {e}")

        try:
            commits_per_day(commits)
        except Exception as e:
            print(f"Error in commits.py -> commit_over_time() \n Error:{e} ")

        try:
            commits_perday_peruser(commits)
        except Exception as a:
            print(f"Error in commits.py -> commit_frequency_per_user()\nError:{e}")
    
        try:
            commit_msg_wordcloud(commits)
        except Exception as t:
            print(f"Error in commits.py -> commit_msg_wordcloud()\nError:{t}")
    else:
        print("No commit data loaded to process.")

if __name__=='__main__':
    
    import requests
    from scripts.variables import var
    
    filename=r'C:\Users\HP\OneDrive\Documents\GithubRepos\Data\commits.json'
    headers = {'Authorization': f'token {var.token}'}
    
    if var.repo:
        print(f"Finding latest commits of {var.repo} repo")
    else:
        var.repo='facebook/react'
        #pass

    print("\n*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=")
    print("Processing the Commits file")
    print("*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=")


    per_page=100
    commits= f'https://api.github.com/repos/{var.repo}/commits?per_page={per_page}'
    response = requests.get(commits, headers=headers)
    
    if response.status_code==200:
        data=response.json()
        print("**************************************")
        print(f"Total {len(data)} commits found")
        print(f"Per_page: {per_page}")
        print("**************************************")

        try:
            path=r'Data'
            os.makedirs(path,exist_ok=True)
            filepath=os.path.join(path,'commits.json')
            with open(filepath,'w') as file:
                json.dump(data, file, indent=4 )
                print("✅ Saved commits.json")
        except:
            print('❌ Failed to save commits.json')

        try:
            processing_commits(filename)
        except Exception as s:
            print(f"Error: {s}")
    
    else:
        print(f"Response code error: {response.status_code}")