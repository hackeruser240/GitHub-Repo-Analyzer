# GitHub Repository Analyzer

This project collects data from any public GitHub repository and gives the health status of any open-source project. Basically, it explores the following:

1. History of commits
2. Most active users

### <u>How it works</u>:

It collects data from two open-source links:

- Contributors: https://api.github.com/repos/facebook/react/contributors
- Commits: https://api.github.com/repos/facebook/react/commits

and consolidates that (JSON) information and presents it in the form of:

1. Streamlit deployed app at [link](https://gh-app-repo-analyzer.streamlit.app/). *The link can be down, Please email if you want it to be active*.
2. Generated PDF
3. Supported images

Additional points:
1. The PDF and supported will be saved in your local computer when run through argparse.
2. When run on streamlit, the PDF will be saved only when using the 'Generate PDF' button.
3. The figures will be displayed on and when run on streamlit.

### <u>File(s) explanation</u>:

1. `main.py`: the file gluing different parts of the program

Files located in `scripts/`:

2. `app.py`: contains `streamlit` app logic
3. `contributors.py`: collects info revolving aroung the contributors
    - top and lowest contributors
    - their respective bar-plot visualizations
4. `commits.py`: collects info regarding the repo's commit data.
    - prints author by greatest commit & timeline →
    - allows in-line (CMD) visualization using python's `tabulate` module
    - produces visualizations:
        * commits per day
        * commits per day per user
        * commit wordcloud
5. `varibales.py`: file containing all the global variables and their docs

### <u>How to run</u>:

1. Fork the repo locally, run it using `streamlit run app.py`. Make sure you have streamlit installed on your system\environment.

2. You can deploy the app using [Streamlit Community Cloud](https://streamlit.io/cloud).

3. Using argparse.
    * You have to run `python main.py -h` for help. It takes repo name as an argument.
    * You can run it two ways: `python main.py --repo facebook/react` or `python main.py --repo https://github.com/facebook/react`. Both will work

### Sample Run:
You may please look at the 'facebook/react' directory to have a look at the output when the script is run through command line.

## Possible Future update(s):

1. Deploy using docker
2. Deploy on a free-hosted cloud service
3. Adjusting more API endpoints