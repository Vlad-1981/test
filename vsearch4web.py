from flask import Flask, render_template, request, escape, session
from vsearch import search4letters
from dbconfig import dbconfig
from DBcm import UserDatabase
from checker import check_logged_in

app = Flask(__name__)

app.secret_key = 'YouWillNeverGuessMySecretKey'


@app.route('/')
@app.route('/index')
def index() -> str:
    return render_template("index.html")


@app.route('/setuser/<user>')
def setuser(user: str) -> str:
    session['user'] = user
    return 'User value set to: ' + session['user']


@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You are now logged in'


@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are now logged out'


@app.route('/status')
def check_status() -> str:
    if 'logged_in' in session:
        return 'You are currently logged in'
    return 'You are NOT logged in'


def log_request(req: 'flask_request', res: str) -> None:
    with UserDatabase(dbconfig) as cursor:
        tuple_ = (req.form['phrase'],
                  req.form['letters'],
                  req.remote_addr,
                  req.user_agent.browser,
                  res,)

        _SQL = """insert into log
                                    (phrase, letters, ip, browser_string, results)
                            values
                                    (%s, %s, %s, %s, %s)"""


def log_request(req: 'flask_request', res: str) -> None:
    with open('vsearch.log', 'a') as log:
        # print(req, res, file=log)
        # print(str(dir(req)), res, file=log)
        print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search4letters(phrase, letters))
    try:
        log_request(request, results)
    except Exception as err:
        print(f"***** Loggin failed with this erroe: {err}")

    return render_template('results.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results, )


@app.route('/entry')
def entry_page() -> 'html':
    return render_template("entry.html",
                           the_title='Welcome to search4letters on the web!')


@app.route('/user')
def user() -> str:
    return render_template("user.html")


@app.route('/registration')
def user_reg() -> str:
    return render_template("registration.html")


@app.route('/about')
def about() -> 'html':
    return render_template("about.html")


@app.route('/new')
def new() -> 'html':
    return render_template("new.html")


@app.route('/Load')
def load() -> 'html':
    return render_template("load.html")


@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for elem in line.split('|'):
                contents[-1].append(escape(elem))
    row_titles = ('Form Data', 'Remote_addr', 'User_agent', 'Results')
    return render_template("viewlog.html",
                           the_title="Обработка данных файла 'viewsearch.log'",
                           the_row_titles=row_titles,
                           the_data=contents)


if __name__ == "__main__":
    app.run(debug=True)

