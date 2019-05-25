# asset-time-machine-app
Python Dash app that lends insight into financial asset performance over time. 

# set-up notes (will clean the README up later)
- all contributors use their own branch (e.g. paul_dev) and submit PRs to master for review and merge to master
- use of virtual environment is recommended (i.e.):
    - `python3 -m venv env`
        - run this in your project working directory
    - `source env/bin/activate`
        - run this to activate the virtual environment
    - `deactivate`
        - run this to deactivate the virtual environment 

- all packages should be documented in the requirements.txt, such that all users are running the same version (i.e.):
    - `pip install -r requirements.txt`
        - run this once you have activated the virtual environment to install all necessary package version
    - `pip freeze > requirements.txt`
        - if you need a new package beyond what is already in this file, pip install the package and then use this command to update the reqs

# preliminary steps
- pick a data source for OHLC stock market data
    - important caveat: I want it to also include index funds, if possible (i.e. VIT, VTV, etc.)
    - figure out how close to live we can get it (maybe via some sort of a streaming API?)
- use a jupyter notebook to test basic data workflow before porting it into the Dash app structure; the .ipynb should contain:
    - data pull
    - any data cleaning / transformation
    - function that takes as its input a stock ticker and a datetime, calculates % down from ATH, and also finds most recent time in history close to that % down from ATH
    - function that produces some time series plot (maybe of closing price?) that clearly shows the % we are down from ATH, and links that back to the most recent time in history where we were close to that same % down from ATH
- begin coding the dash app
    - most basic version should have 2 call-back selectors--one for the asset, and one for the selected datetime of interest (but the user should also be able to select the later by clicking on the aforementioned chart)