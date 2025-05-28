import os
import sys

from contextlib import contextmanager
from scripts.variables import var

'''
Functions most probablt that will be used in main.py
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