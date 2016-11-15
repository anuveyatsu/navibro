# SuperNavi3333

SuperNavi3333 is an app created with Python 3.5.2 and Flask framework.
The app searches github repositories for given search term.
It sorts results by created date in descending order.
Then it takes latest 5 results and renders them in html format.
Due to 6 API calls being made, rendering page may take around 10-20 seconds.

Before getting started make sure you have correct version of Python installed.
Also, you will need package management system, 'pip' is used in the instruction below.

**This package includes:**
a) app.py -- solution
b) templates/template.html -- the template file
c) dependencies -- all required dependencies
d) cover.txt -- this file (includes description and instructions)

e) test.py -- unit tests using unittest, flask_testing extension, and vcrpy
f) fixtures folder -- contains vcr_cassettes

### Running SuperNavi3333 locally

You can run SuperNavi3333 on your machine by following steps below:

##### 1) Setup virtual environment

If you do not have a Virtual Environment installed:

  $ pip install virtualenv

Go to downloaded folder:

  $ cd SuperNavi3333-master

Setup a Virtual Environment for this project:

  $ virtualenv SuperNavi3333

##### 2) Activate your virutal environment

  $ source SuperNavi3333/bin/activate

##### 3) Install all dependencies

  $ pip install -r dependencies

##### 4) Run unit tests
Note that this test uses recorded VCR cassettes.
If you wish to run this test without cassettes then just delete all files in /fixtures/vcr_cassettes folder.

  $ python test.py -v

##### 5) Run app on localhost

  $ python app.py

##### 6) Go to address given

  http://127.0.0.1:5000 (or check yours)

##### 7) Enter some request

  http://127.0.0.1:5000/navigator?search_term=arrow
