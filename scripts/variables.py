import os
from dotenv import load_dotenv

load_dotenv()

class Variables:
    def __init__(self):
        self.token=os.getenv("GITHUB_TOKEN")
        self.headers = {'Authorization': f'token {self.token}'}