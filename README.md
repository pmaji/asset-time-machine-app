# asset-time-machine-app
Early work in progress. Check back frequently for updates and new additions. 

# set-up notes (will clean the README up later)
- all contributors use their own branch (e.g. paul_dev) and submit PRs to master for review and merge to master
    - create a branch and named it *your_firstname_here*_dev
    - clone that branch locally
    - to test that it worked:
        - make a small test change to a file like the README
        - save
        - `git add --all`
        - `git commit -m "use some simple imperative commit message here"`
        - `git push`
        - go back to your branch on github via the GUI and submit a pull request
        - once it is approved and merged, go back to your terminal and run `git pull`
        - once that is complete--you should see "Fast-forward" in your terminal once it's done--run `git merge origin/master` to ensure you are up to date with master locally
        - after the merge completes, when you go back to your branch on github's gui you should see "This branch is even with master." right underneath your branch name
        - congrats! you now have working branched version control and are ready to get developping! 
- use of virtual environment is recommended, i.e.:
    - `python3 -m venv env`
        - run this in your project working directory to create the virutal environment and name it "env" (standard convention)
    - `source env/bin/activate`
        - run this to activate the virtual environment
    - `deactivate`
        - run this to deactivate the virtual environment 

- all packages should be documented in the requirements.txt file, so that all users are running the same package versions, i.e.:
    - `pip install -r requirements.txt`
        - run this once you have activated the virtual environment to install all necessary package versions
    - `pip freeze > requirements.txt`
        - if you need a new package beyond what is already in the extant requirements.txt file, pip install the package and then use this command to update the reqs

# preliminary steps
- pick a data source for OHLC stock market data
    - important caveat: I want it to also include index funds, if possible (i.e. VTI, VTV, etc.)
    - figure out how close to live we can get it (maybe via some sort of a streaming API call?)
- use a jupyter notebook to test basic data workflow before porting it into the Dash app structure; the .ipynb should contain:
    - data pull
    - any data cleaning / transformation
    - function that takes as its input a stock ticker and a datetime, and calculates % down from all-time-high (henceforth ATH), and also finds most recent time in history close to that % down from ATH
    - function that produces some time series plot (maybe of closing price?) that clearly shows the % we are down from ATH, and links that back to the most recent time in history where we were close to that same % down from ATH
- begin coding the dash app
    - most basic version should have 1 call-back selector--the selector for the asset of interest (i.e. VTI or GOOGL)
# later steps to come
- pick dashboard format and maybe copy some css / js from the plotly dash library of examplars 
- write better narrative README and docs 
- thing about integrating cryptos as well
- build all elements of main GUI; right now I'm thinking:
    - asset-selector at the top
    - 1st main chart is closing price over time 
    - 2nd main chart underneath is % down from ATH over time
    - 3rd main component is a table that updates with whatever date is selected, and includes things like:
        - each row is an instance of a past time in history when this asset was the same % down from ATH
        - columns for what % gain / loss was realized starting at that historical point, looking forward 10. 30. 60 days etc.
        - column for number of days until the next all-time-high 
    - some similar vizs / apps for inspiration:
        - [example Dash app for financial asset tracking](https://github.com/plotly/dash-stock-tickers-demo-app)


# developers on this project:
- [Paul Jeffries](https://twitter.com/ByPaulJ)
- [Zach Hall] (https://cdn.shopify.com/s/files/1/1195/1382/products/thug-life-bear-sticker-riot-society-clothing_2000x.jpg?v=1548319485)