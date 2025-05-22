import os
from dotenv import load_dotenv

load_dotenv()

class Variables:
    def __init__(self):
        self.repo=None
        self.token=os.getenv("GITHUB_TOKEN")
        self.headers = {'Authorization': f'token {self.token}'}

        '''
        lowest_contributions: int
        Give me the number of users with commits < lowest_contributions

        top_contributors: int
        Give the top 'top_contributors' contributors
        '''
        self.lowest_contributions=100
        self.top_contributors=10

        '''
        authors: dict
        defined in commits.py
        extracts the the list of authors of the commits of the github repo and counts each of their respective commits

        raw_authors: list
        defined in commits.py
        extracts the raw author names from commits.json and stores them in the list
        '''
        self.authors={}
        self.raw_authors=[]
        
        '''
        defined in commits.py
        used in commit_title_visualization()
        stores the clean titles of the latest commits made in the repo
        '''
        self.commit_titles=[]

        '''
        
        '''
        self.path=r'Data'
        self.save_dir=''

var=Variables()