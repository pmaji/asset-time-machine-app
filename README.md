# Asset Time Machine App

## Overview

*All views expressed on this site are my own and do not represent the opinions of any entity with which I have been, am now, or will be affiliated.*

Early work in progress. Check back frequently for updates and new additions. 

Here is a teaser of the kinds of charts the app allows you to explore:
![Basic Asset Viz.](https://raw.githubusercontent.com/pmaji/asset-time-machine-app/master/media/test_vti_chart_screenshot_july62019.jpg)

If you have questions, comments, or suggested alterations to these materials, please [open an issue here](https://github.com/pmaji/asset-time-machine-app/issues) on GitHub. Also, don't hesitate to reach out [via Twitter here](https://twitter.com/ByPaulJ).

## Setup

All environment management for this project is accomplished via [Anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html). Once you have cloned the repository locally, there are a few simple steps to get up and running; just run the code snippets below in terminal.

- environment setup:
    - `conda env create -f environment.yml`
        - this code builds the conda virtual environment (named "atm_env") with all necessary dependencies 
    - `conda activate atm_env`
        - this code activates the environment so that you can start running code or the app itself
- running the code & app:
    - `jupyter lab`
        - this code will spin up a [Jupyter Lab](https://jupyterlab.readthedocs.io/en/stable/) instance for interactive editing, with all settings and packages loaded
    - `python app.py`
        - this code will launch the app locally

## Contribution Rules
    
If interested in contributing to this project, check out the [open issues](https://github.com/pmaji/asset-time-machine-app/issues) to see what we have on deck for development where you might be able to pitch in. If you have other suggestions for development or ways you'd like to contribute, please open an issue to get that conversation started. 

Presently there are two main developers working on the project:
- [Paul Jeffries](https://twitter.com/ByPaulJ)
- [Zach Hall](https://cdn.shopify.com/s/files/1/1195/1382/products/thug-life-bear-sticker-riot-society-clothing_2000x.jpg?v=1548319485)

All contributors should use their own branch (e.g. paul_dev) unless the planned contribution is small (i.e. limited to a one-off PR). Development work should be done in the dev branches, with PRs then being submitted to master for review and subsequent merging. For anyone seeking to contribute who is not familiar with GitHub, feel free to look over the basic instructions below to get started. 

- create a branch and name it <yournamehere_dev>
- clone that branch locally
- to confirm that you're all set up:
    - make a small test change to a file like the README.md
    - save your changes and run the following code in your terminal
    - `git add --all`
    - `git commit -m "use some simple imperative commit message here"`
    - `git push`
    - go back to your branch on GitHub via the GUI and submit a pull request
    - once it is approved and merged, go back to your terminal and run `git pull`
    - once that is complete--you should see "Fast-forward" in your terminal once it's done
    - run `git merge origin/master` to ensure you are up to date with master locally
    - if the merge works, you should see "This branch is even with master." under your branch name on GitHub's GUI
    - congrats; you now have working branched version control and are ready to get developping!
