import os
import sys

from contextlib import contextmanager
from scripts.variables import var
import matplotlib.pyplot as plt

'''
Used in:

main.py
savetoPDF.py
'''
def make_repo_folder():
    folder_name=var.repo.split("/")[0] + "-" + var.repo.split("/")[1]
    os.makedirs(folder_name,exist_ok=True)
    return folder_name

'''
main.py:
'''

@contextmanager
def suppress_stdout(enabled=True):
    if enabled:
        yield
    else:
        with open(os.devnull, 'w',encoding="utf-8") as devnull:
            original_stdout = sys.stdout
            sys.stdout = devnull
            try:
                yield
            finally:
                sys.stdout = original_stdout

'''
Used in:
commits.py
contributors.py
'''
def save_fig(name):
    if not name or isinstance(name,str):
        folder = os.path.join(make_repo_folder(), var.path)
        os.makedirs(folder, exist_ok=True)  # ✅ Creates just the folders
        filepath = os.path.join(folder, name)
        plt.savefig(filepath, dpi=300)

'''
used in:

'''

def get_logger(use_streamlit=False, output_area=None):
    def log(msg):
        if use_streamlit and output_area is not None:
            output_area.write(msg)
        else:
            print(msg)
    return log
