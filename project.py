#!/usr/bin/env python

## ==================================
## === packages, modules, pragmas ===
## ==================================

## === built-ins ===
import cgi
import sys
import os                                                   # used to obtain environment host name & process web file paths
import argparse                                             # used when running as script; should be moved to DAO
import logging
import logging.config                                       # pythons logging feature
from mimetypes import types_map                             # for processing additional files

## === 3rd party ===
from flask import Flask, request, render_template, url_for, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

## === custom ===
from database_setup import Base, Asset, Allocation
# import pymongo
# import json
# from tornado.ioloop import IOLoop
# #from tornado.log import enable_pretty_logging
# #import tornado.options
# from tornado.web import RequestHandler, Application, url, RedirectHandler, StaticFileHandler
# from tornado.httpclient import AsyncHTTPClient
# from tornado.escape import json_decode
# from tornado import gen
# #import tornado.logging
# #import tornado.web.authenticated (decorator for ensuring user is logged in)
#
## ===============================
## === command-line processing ===
## ===============================

parser = argparse.ArgumentParser()
parser.add_argument('--port',           default=8000,                           help="sets port number for web service")
parser.add_argument('--host',           default='localhost',                    help="sets host for web service")
parser.add_argument('--log_file',       default='log/web.log',                  help="path/file for logging")
parser.add_argument('--start',          dest='start',   action='store_true',    help="start the server")
parser.add_argument('--app',            default='simco_app',                    help="name of application")
parser.add_argument('--debug',          dest='debug',   action='store_true',    help="sets server debug, and level of logging")
parser.add_argument('--db',             default='sqlite:///simco.db',           help="designates the database to use")

args        = parser.parse_args()

def pargs():
    '''prints items in args object for ease of reading'''
    print('\n')
    for item in args._get_kwargs():
        k,v = item
        print('\t' + k + ': ' + str(v))

## ===================================
## === logging to file and console ===
## ===================================

ERROR_FORMAT        = "%(asctime)s %(name)s %(levelname)-8s %(message)s"
INFO_FORMAT         = "%(asctime)s %(name)s %(levelname)-8s %(message)s"
CONSOLE_FORMAT      = "\n\t%(message)s"
if args.debug == True:
    DEBUG_FORMAT    = "%(asctime)s %(name)s %(levelname)-8s %(filename)s->%(funcName)s line %(lineno)d: %(message)s"
    LOG_LEVEL       = "DEBUG"
else:
    DEBUG_FORMAT    = INFO_FORMAT
    LOG_LEVEL       = "INFO"
LOG_CONFIG = {'version':1,
              'formatters':{'error':{'format':ERROR_FORMAT},
                            'info':{'format':INFO_FORMAT},
                            'console':{'format':CONSOLE_FORMAT},
                            'debug':{'format':DEBUG_FORMAT}},
              'handlers':{'console':{'class':'logging.StreamHandler',
                                     'formatter':'console',
                                     'level':logging.DEBUG},
                          'file':{'class':'logging.FileHandler',
                                  'filename':args.log_file,
                                  'formatter':'debug',
                                  'level':logging.INFO}},
              'root':{'handlers':['console', 'file'], 'level':LOG_LEVEL}}
logging.config.dictConfig(LOG_CONFIG)
logger      = logging.getLogger(args.app)

## ====================
## == db connection ==
## ===================

try:
    session     = sessionmaker()(bind=create_engine(args.db))
    assets      = session.query(Asset)                                   # load global objects for convenience
    logger.info("assets loaded: {}".format(str(len(list(assets)))))
    allocations = session.query(Allocation)
    logger.info("allocations loaded: {}".format(str(len(list(allocations)))))
except:
    logger.exception("issue loading database items", exc_info=1)

# ## ============
# ## == Routes ==
# ## ============

app = Flask(__name__)

@app.route('/')
#@app.route('/assets')
def showAssets_plain():
    '''show assets, no css template'''
    asset_list = [" id\texchange\tsymbol\t\description\tsize"]
    for item in assets:
        asset_list.append('{0}\t<a href="/assets/{0}/">{1}</a>\t{2}\t{3}'.format(str(item.id), item.exchange, item.symbol, item.description, item.size))
        output = '<br>'.join(sorted(asset_list))
#    return ('list of assets\nsymbol\tdescription\texchange')output   # need to handle case when assets is not populated
    return output   # need to handle case when assets is not populated

@app.route('/assets')
def showAssets():
    '''show Assets'''
    return render_template('assets.html', assets=assets)

@app.route('/assets/<int:asset_id>/')
def showAssets2(asset_id):
    '''show Asset'''
    asset = assets.filter_by(id = asset_id).one()
    rest_items = mi.filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=rest_items)

@app.route('/allocations/', methods=['GET', 'POST'])
def showAllocations():
    '''show allocations'''
    return render_template('allocations.html', allocations=allocations)
#    return render_template('restaurants.html', restaurants=rest)

@app.route('/assets/new/', methods=['GET', 'POST'])
def newAsset():
    '''add new asset'''
    if request.method == 'POST':
        asset = Asset(symbol=request.form['symbol'])
        logger.debug('adding new asset', asset.symbol)
        session.add(asset)
        session.commit()
        return redirect(url_for('showAssets'))
    else:
        return render_template('newAsset.html')
    return "page to create a new allocation"

@app.route('/assets/<int:asset_id>/edit/', methods=['GET', 'POST'])
def editAsset(asset_id):
    '''edit asset'''
    if request.method == 'POST':
        asset = assets.filter_by(id = asset_id).one()
        asset.asset_id = request.form['asset id']
        logger.debug('updating asset', asset.asset_id)
        session.add(asset)
        session.commit()
        return redirect(url_for('showAssets'))
    else:
        return render_template('editAsset.html', asset=assets.filter_by(id=asset_id).one())
    return "page to edit asset"

@app.route('/assets/<int:asset_id>/delete/', methods=['GET', 'POST'])
def deleteAsset(asset_id):
    '''delete asset'''
    if request.method == 'POST':
        asset = assets.filter_by(id = asset_id).one()
        logger.debug('deleting asset', asset.id)
        session.delete(asset)
        session.commit()
        return redirect(url_for('showAssets'))
    else:
        return render_template('deleteAsset.html', asset=assets.filter_by(id=asset_id).one())
    return "page to delete asset"

@app.route('/allocations/new/', methods=['GET', 'POST'])
def newAllocation():
    '''add new allocation'''
    if request.method == 'POST':
        allocation = Allocation(name=request.form['name'])
        logger.debug('adding new allocation', allocation.name)
        session.add(allocation)
        session.commit()
        return redirect(url_for('showAllocations'))
    else:
        return render_template('newAllocation.html')
    return "page to create a new allocation"

@app.route('/allocations/<int:allocation_id>/edit/', methods=['GET', 'POST'])
def editAllocation(allocation_id):
    '''edit allocation'''
    if request.method == 'POST':
        allocation = allocations.filter_by(id = allocation).one()
        allocation.asset_id = request.form['asset id']
        logger.debug('updating allocation', allocation.asset_id)
        session.add(allocation)
        session.commit()
        return redirect(url_for('showAllocations'))
    else:
        return render_template('editAllocation.html', allocation=allocations.filter_by(id=allocation_id).one())
    return "page to edit allocation"

@app.route('/allocations/<int:allocation_id>/delete/', methods=['GET', 'POST'])
def deleteAllocation(allocation_id):
    '''delete allocation'''
    if request.method == 'POST':
        allocation = allocations.filter_by(id = allocation_id).one()
        logger.debug('deleting allocation', allocation.id)
        session.delete(allocation)
        session.commit()
        return redirect(url_for('showAllocations'))
    else:
        return render_template('deleteAllocation.html', allocation=allocations.filter_by(id=allocation_id).one())
    return "page to delete allocation"


# === old stuff ===

@app.route('/restaurants/<int:restaurant_id>/')
def showMenu(restaurant_id):
    '''show restaurant menu'''
    restaurant = rest.filter_by(id = restaurant_id).one()
    rest_items = mi.filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=rest_items)

@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant():
    '''add new restaurant'''
    if request.method == 'POST':
        restaurant = Restaurant(name=request.form['name'])
#        newRestaurant = Restaurant(name=request.form['name'][0].decode('ascii'))
        logger.debug('adding new restaurant', restaurant.name)
        session.add(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')
    return "page to create a new restaurant"

@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    '''edit restaurant'''
    if request.method == 'POST':
        restaurant = rest.filter_by(id = restaurant_id).one()
        restaurant.name = request.form['name']
        logger.debug('updating restaurant', restaurant.name)
        session.add(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant=rest.filter_by(id=restaurant_id).one())
    return "page to edit restaurant"

@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    '''delete restaurant'''
    if request.method == 'POST':
        restaurant = rest.filter_by(id = restaurant_id).one()
        logger.debug('deleting restaurant', restaurant.name)
        session.delete(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant=rest.filter_by(id=restaurant_id).one())
    return "page to delete restaurant"

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    '''add new menu items'''
    if request.method == 'POST':
        menuitem = MenuItem(name=request.form['name'], price=request.form['price'], desc=request.form['desc'])
#        newRestaurant = Restaurant(name=request.form['name'][0].decode('ascii'))
        logger.debug('adding new menu item', menuitem.name)
        session.add(menuitem)
        session.commit()
#        return redirect(url_for('showRestaurants'))
        return redirect(url_for('showMenu') + '/' + restaurant_id)
    else:
        return render_template('newmenuitem.html')
    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    '''edit menu items'''
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    '''delete menu items'''
    return "page to delete a menu item. Task 3 complete!"

# ## =============
# ## == classes ==
# ## =============

# ## ==========
# ## == main ==
# ## ==========

def main():
    app.debug == args.debug
    app.run(host = args.host, port = args.port)


# ## ============
# ## == module ==
# ## ============

if args.start   == True:
    main()
