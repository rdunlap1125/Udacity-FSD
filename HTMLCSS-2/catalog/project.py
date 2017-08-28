from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash
import json

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

from flask import session as login_session

import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2

from flask import make_response
import requests

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# HELPER FUNCTIONS


def buildInvalidStateResponse():
    response = make_response(json.dumps('Invalid state parameter.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response


def createUser(login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# JSON APIs


# JSON API for the catalog home page
# Returns a list of all categories and a list of the last 9 items added
@app.route('/catalog/JSON')
def catalogJSON():
    categories = session.query(Category).order_by(asc(Category.name))
    latestItems = session.query(Item).order_by(desc(Item.added)).limit(9)
    return jsonify(
        categories=[c.serialize for c in categories],
        latestItems=[i.serialize for i in latestItems])


# JSON API for a specific category
# Returns a list of all categories (just like the page),
# the selected category and a list of all items in the category
@app.route('/catalog/<string:category_name>/JSON')
@app.route('/catalog/<string:category_name>/items/JSON')
def categoryJSON(category_name):
    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(Item).join(Category).filter(
        Category.name == category_name).all()
    return jsonify(
        categories=[c.serialize for c in categories],
        selectedCategory=category_name,
        items=[i.serialize for i in items])


# JSON API for a specific item
@app.route('/catalog/<string:category_name>/<string:item_name>/JSON')
def itemJSON(category_name, item_name):
    item = session.query(Item).join(Category).filter(
        Item.name == item_name, Category.name == category_name).one()
    return jsonify(item=item.serialize)


# WEB PAGE METHODS


# Show all categoriesand the last 9 items added to the system
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    login_session['last_url'] = request.url
    categories = session.query(Category).order_by(asc(Category.name))
    latestItems = session.query(Item).order_by(desc(Item.added)).limit(9)
    return render_template('catalog.html',
                           pagename="Catalog",
                           categories=categories,
                           latestItems=latestItems)


# Show a particular category
# If a user is logged in, they can create new items for the category
@app.route('/catalog/<string:category_name>/')
@app.route('/catalog/<string:category_name>/items/')
def showCategory(category_name):
    login_session['last_url'] = request.url
    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(Item).join(Category).filter(
        Category.name == category_name).all()
    editable = 'username' in login_session
    return render_template('category.html',
                           pagename=category_name,
                           categories=categories,
                           category_name=category_name,
                           items=items,
                           editable=editable)


# Show a particular item
# If a user is logged in and owns this item, they can update or delete the item
@app.route('/catalog/<string:category_name>/<string:item_name>/')
def showItem(category_name, item_name):
    login_session['last_url'] = request.url
    item = session.query(Item).join(Category).filter(
        Item.name == item_name, Category.name == category_name).one()
    editable = ('username' in login_session and
                item.user_id == login_session['user_id'])
    return render_template('item.html',
                           pagename=item.name,
                           item=item,
                           editable=editable)


# Create a new item -- requires the user to be logged in
@app.route('/catalog/<string:category_name>/new', methods=['GET', 'POST'])
@app.route('/catalog/<string:category_name>/items/new',
           methods=['GET', 'POST'])
def newItem(category_name):
    login_session['last_url'] = request.url
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(name=category_name).one()
    if request.method == 'POST':
        itemName = request.form['name']
        existingItemCount = session.query(Item).filter_by(
            name=itemName).count()
        if existingItemCount != 0:
            flash('Item %s already exists!' % itemName)
            return redirect(
                url_for('showCategory', category_name=category_name))
        item = Item(name=request.form['name'],
                    description=request.form['description'],
                    category_id=category.id,
                    user_id=login_session['user_id'])
        session.add(item)
        session.commit()
        flash('New item %s successfully created' % (item.name))
        return redirect(url_for('showCategory', category_name=category_name))
    else:
        return render_template('newItem.html', category=category)


# Edit an item
# -- requires the user to be logged in and to be the owner of the item
@app.route('/catalog/<string:category_name>/<string:item_name>/edit',
           methods=['GET', 'POST'])
def editItem(category_name, item_name):
    login_session['last_url'] = request.url
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(Item).join(Category).filter(
        Item.name == item_name, Category.name == category_name).one()
    if login_session['user_id'] != item.user_id:
        flash('Not authorized to edit item %s!' % item_name)
        return redirect(url_for(
            'showItem', category_name=category_name, item_name=item.name))
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        session.add(item)
        session.commit()
        flash('Item %s successfully edited' % (item.name))
        return redirect(url_for(
            'showItem', category_name=category_name, item_name=item.name))
    else:
        return render_template('editItem.html', item=item)


# Delete an item
# -- requires the user to be logged in and to be the owner of the item
@app.route('/catalog/<string:category_name>/<string:item_name>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    login_session['last_url'] = request.url
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).join(Category).filter(
        Item.name == item_name, Category.name == category_name).one()
    if login_session['user_id'] != item.user_id:
        flash('Not authorized to delete item %s!' % item_name)
        return redirect(url_for(
            'showItem', category_name=category_name, item_name=item.name))
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Item %s successfully deleted' % (item.name))
        return redirect(url_for('showCategory', category_name=category_name))
    else:
        return render_template('deleteItem.html', item=item)


# CONNECTION MANAGEMENT METHODS


# Login and create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# FB connect method built out during the course
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        return buildInvalidStateResponse()

    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = ('https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s'
           % (app_id, app_secret, access_token))
    result = httplib2.Http().request(url, 'GET')[1]

    # Use token to get user info from API
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = ('https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email'
           % token)
    result = httplib2.Http().request(url, 'GET')[1]
    data = json.loads(result)

    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    flash("Now logged in as %s" % login_session['username'])
    return "Successful FB login!"


# FB disconnect method built out during course
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must be included to successfully logout
    access_token = login_session['access_token']
    url = ('https://graph.facebook.com/%s/permissions?access_token=%s'
           % (facebook_id, access_token))
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['facebook_id']
    return "you have been logged out"


# Google connect method built out during course
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        return buildInvalidStateResponse()

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(
            'goog_client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != json.loads(
      open('goog_client_secrets.json', 'r').read())['web']['client_id']:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    flash("you are now logged in as %s" % login_session['username'])

    return "Successful Google login!"


# Google disconnect method built out during course
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Disconnect based on provider
@app.route('/logout')
def logout():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        if login_session['provider'] == 'facebook':
            fbdisconnect()
        del login_session['username']
        del login_session['email']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCatalog'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
