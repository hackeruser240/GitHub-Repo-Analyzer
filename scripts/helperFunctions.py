import os
from scripts.variables import var

def make_repo_folder():
    folder_name=var.repo.split("/")[0] + "-" + var.repo.split("/")[1]
    os.makedirs(folder_name,exist_ok=True)
    return folder_name