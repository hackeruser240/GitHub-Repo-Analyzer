import os
from dotenv import load_dotenv

load_dotenv()

class Variables:
    @staticmethod
    def get_github_token():
        try:
            import streamlit as st
            return st.secrets["GITHUB_TOKEN"]
        except (ImportError,KeyError):
            from dotenv import load_dotenv
            load_dotenv()
            return os.getenv("GITHUB_TOKEN")
    
    def __init__(self):     
        self.token=self.get_github_token()
        self.repo=None        
        self.headers = {'Authorization': f'token {self.token}'}

        '''
        numof_lowest_contributions: int
        Give me the number of users with commits < lowest_contributions

        numof_top_contributors: int
        Give the top 'top_contributors' contributors
        '''
        self.numof_lowest_contributions=100
        self.numof_top_contributors=10

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
        used in:
        initializes the respective variables
        '''
        self.path=r'images'
        self.save_dir=''


        '''
        defined in contributors.py
        
        used in top_contributors()
        used to store the top contributors (by default, 100)

        used in lowest_contributors()
        used to store the lowest contribution (by default, <100)
        '''
        self.top_contributors=[]
        self.lowest_contribution=[]

        '''
        Used in main.py
        An empty container used to store the response.json
        '''
        self.contributors_data=[]

        '''
        used in main.py to store open and closed issues respectively
        '''
        self.open_issues=None
        self.closed_issues=None
var=Variables()