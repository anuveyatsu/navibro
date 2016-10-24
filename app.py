""" This code is written in Python 3.5.2.
The app searches github repositories for given search term.
It sorts results by created date in descending order.
Then it takes latest 5 results and renders them in html format."""

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    """ This is home page. It returns welcoming message. """
    return 'Hi there! Go to "/navigator" and pass "search_term" parameter'

@app.route('/navigator')
def navigator():
    """ This is main method that returns rendered template. """
    if 'search_term' in request.args and request.args['search_term'] != '':
        res = github_repo(request.args['search_term'])
        if 'try again' not in res:
            search_info = {'search_term': request.args['search_term'],
                           'total_count': res['total_count'],
                           'incomplete_results': res['incomplete_results']}
            sorted_res = sort_desc(res['items'], 'created_at')
            first_5_res = first_5_items(sorted_res)
            for i in first_5_res:
                last_commit = github_commits(i['full_name'])
                if last_commit == 'n/a':
                    i['sha'] = i['commit_message'] = i['commit_author_name'] = last_commit
                else:
                    i['sha'] = last_commit['sha']
                    i['commit_message'] = last_commit['commit']['message']
                    i['commit_author_name'] = last_commit['commit']['author']['name']
            return render_template('template.html', data=first_5_res, search_info=search_info)
        else:
            return 'Oops... server did not response as expected.'
    else:
        return 'provide a search_term'

def github_repo(term):
    """ This method searches for given term in github repositories. """
    url = 'https://api.github.com/search/repositories'
    res = requests.get(url, params={'q': term})
    if res.status_code == 200 and len(res.json()) == 3:
        return res.json()
    else:
        return ('try again because ' +
		              '1) you did not pass a search term; ' +
				            '2) something wrong on the server')

def github_commits(repo):
    """ This method searches a given repository commits and returns latest one. """
    url = 'https://api.github.com/repos/' + repo + '/commits'
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()[0]
    else:
        return 'n/a'

def sort_desc(data, term):
    """ This method sorts passed data by passed term in descending order. """
    return sorted(data, key=lambda k: k[term], reverse=True)

def first_5_items(data):
    """ This method returns first 5 items of given list. """
    return data[:5]


if __name__ == '__main__':
    app.run(debug=True)
