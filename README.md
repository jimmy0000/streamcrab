Streamcrab
==========

Streamcrab is a quasi-realtime twitter sentiment analyzer

This is the second version of the tool, and it is rewritten completely from previous version
(still available in legacy branch)

Features and Changes from legacy version
----------------------------------------

- Switched to MaxEnt as default classifier
- Simplified tweets collection (see `Collecting raw Tweets`)
- Simplified trainer (see `Train classifier`)
- Build in HTTP server & Frontend
- Unittests tested
- Utilization of multi-core systems
- Scalable (in theory :)


Requirements
------------

- python 2.7
- python2.7-dev
- mongodb server


Debian like systems:

    apt-get install python2.7 python2.7-dev mongodb-server


Checkout
--------
Checkout latest streamcrab branch from github


    git clone git@github.com:cyhex/streamcrab.git ./streamcrab
    cd streamcrab


Configure
---------
copy smm/config.default.py to smm/config.py and edit smm/config.py according to your needs

    cp smm/config.default.py smm/config.py
    nano smm/config.py


Installation & Setup
--------------------
Download and install required libs and data

    python setup.py develop
    python toolbox/setup-app.py



Testing
-------
Run unittests

    python -m unittest discover tests


Collecting raw Tweets
---------------------
The base of data training is an assumption that tweets with happy emoticons :) are positive and tweets
with sad :( emoticons have negative sentiment polarity

Wether this assumption is correct or not is outside the scope of this document.

Collect 2000 'happy' tweets

    python toolbox/collect-tweets.py happy 2000

Collect 2000 'sad' tweets

    python toolbox/collect-tweets.py sad 2000

for more options see

    python toolbox/collect-classifier.py --help


Train classifier
----------------
Create and save new classifier trained from collected tweets

    python toolbox/train-classifier.py maxEntTestCorpus 2000

for more options see

    python toolbox/train-classifier.py --help



Show stats
----------
Show detailed info on collected Tweets and saved classifiers

    python toolbox/show-classifiers.py




Training and testing corpora
----------------------------


    http://mpqa.cs.pitt.edu/
    http://nlp.stanford.edu/sentiment/index.html
    http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html#datasets
    http://www.cs.york.ac.uk/semeval-2013/semeval2013.tgz ?

