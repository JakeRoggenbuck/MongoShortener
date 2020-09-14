from flask import Flask, request, render_template
from database import Database


APP = Flask(__name__)
DATABASE = Database()
DATABASE.connect()


@APP.route('/')
def index():
    """Return main page"""
    return render_template('home.html')


@APP.route('/<string:alias>')
def get(alias):
    """Get alias from route and get url, then generate link page"""
    url = DATABASE.get_url(alias)
    # Check if url was returned
    if url is not False:
        # Give url to template
        return render_template('link.html', url=url)
    return "Error"


@APP.route('/new/')
def new_short():
    """Render form from new route"""
    return render_template('form.html')


@APP.route('/new/', methods=['POST'])
def new_short_post():
    """Get post request from new route, send alias and url to database

    Get alias and url from post, add alias to database, render success template
    if alias was successfully created, else return error message"""
    alias = request.form['alias']
    url = request.form['url']
    # Send alias and url to database
    write = DATABASE.add_alias(alias, url)
    if write is not False:
        return render_template('success.html', _alias=alias, _url=url)
    else:
        return render_template('error.html', _alias=alias)


if __name__ == '__main__':
    APP.run()
