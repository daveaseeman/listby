import os
from pocketapp import get_request_token, get_auth_url, get_access_token
from pocketapp import get_list
from flask import Flask, render_template, session, request, url_for

app = Flask(__name__)
app.secret_key = os.urandom(24)

consumer_key = os.environ['POCKET_SECRET']
app_base_url = 'https://listby.herokuapp.com'
redirect = '/account'
redirect_uri = app_base_url + redirect


@app.route('/')
def index():
    if 'user_name' in session:
        return redirect(url_for('account'))
    request_token = get_request_token(consumer_key, redirect_uri)
    session['request_token'] = request_token
    auth_url = get_auth_url(request_token, redirect_uri)
    return render_template('index.html', auth_url=auth_url)


@app.route(redirect)
def account():
    if 'user_name' in session:
        user_name = session['user_name']
        return render_template('account.html', user_name=user_name)
    request_token = session['request_token']
    user_info = get_access_token(consumer_key, request_token)
    access_token = user_info['access_token']
    user_name = user_info['user_name']
    session['access_token'] = access_token
    session['user_name'] = user_name
    return render_template('account.html', user_name=user_name)


@app.route('/list')
def list():
    access_token = session['access_token']
    user_name = session['user_name']
    tag = request.values.get('tag')
    count = request.values.get('count')
    state = request.values.get('state')
    list = get_list(consumer_key, access_token, count, tag, state)
    return render_template('list.html', tag=tag, list=list, user_name=user_name)


@app.route('/logout')
def logout():
    session.pop('user_name', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
