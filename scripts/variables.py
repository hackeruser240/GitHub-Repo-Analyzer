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
        '''
        self.authors={}

var=Variables()