#!/usr/bin/env python

## ==================================
## === packages, modules, pragmas ===
## ==================================

## === built-ins ===
import cgi
import sys
import os                                                   # used to obtain environment host name & process web file paths
import argparse                                             # used when running as script; should be moved to DAO

## === 3rd party ===
from flask import Flask, request, render_template, url_for, redirect, jsonify
import pandas as pd

## === custom ===
import util
from database_setup import Base, Asset, Allocation, createDBsession, RefData

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

util.setLogLevel(args.debug, args.log_file)
logger = util.logging.getLogger(args.app)
logger.info("set logger for app {0} - debug level as {1} using logfile: {2}".format(args.app, args.debug, args.log_file))

## ====================
## == db connection ==
## ===================

try:
    session     = createDBsession(args.db)
    assets      = session.query(Asset)                                   # load global objects for convenience
    logger.info("assets loaded: {}".format(str(len(list(assets)))))
    allocations = session.query(Allocation)
    logger.info("allocations loaded: {}".format(str(len(list(allocations)))))
except:
    logger.exception("issue loading database items", exc_info=1)

# == support functions
def getDF(start_date=None, days=None, mean=False):
    '''setup allocation history, with options for: filtering by start_date, calculating mean'''
    currentAllocations      = list(session.query(Asset.symbol, Allocation.allocation, Allocation.date_mod).join(Allocation))
    allocationsDF           = pd.DataFrame(currentAllocations)
    allocationsDF.date_mod  = pd.to_datetime(allocationsDF['date_mod'])
    if start_date == None:
        result = allocationsDF
    elif days == None:
        result = allocationsDF[allocationsDF.date_mod > start_date]
    else:
        end_date = util.displayTime(start_date, days)
        result = allocationsDF[(allocationsDF.date_mod > start_date) & (allocationsDF.date_mod < end_date)]
    if mean == True:
        result = result.groupby(['symbol']).mean().to_dict().values()
        return [{'symbol':k, 'ave_alloc':v} for k,v in list(result)[0].items()]
        #newdict = list(result.groupby(['symbol']).mean().to_dict().values())[0]
    else:
        result = result.to_dict('records')
        for item in result:
            item['date_mod'] = item['date_mod'].strftime('%Y-%m-%d')
        return result

## ============
## == Routes ==
## ============

app = Flask(__name__)

@app.before_request
def log_request_info():
    logger.debug('Headers: %s', request.headers)
    logger.debug('Body: %s', request.get_data())

@app.route('/')
@app.route('/assets')
def showAssets():
    '''show Assets'''
    return render_template('assets.html', assets = assets)

@app.route('/listAllocations')
def curAllocations():
    '''do join to get current allocations by symbol'''
    result = getDF(start_date, days, mean)
    return jsonify(result)

@app.route('/allocations/', methods = ['GET', 'POST'])
def showAllocations():
    '''show allocations'''
    return render_template('allocations.html', allocations = allocations)

@app.route('/test_form/', methods = ['GET', 'POST'])
def editTest():
    '''edit Test'''
    return render_template('test_form.html')

@app.route('/assets/new/', methods = ['GET', 'POST'])
def newAsset():
    '''add new asset'''
    if request.method == 'POST':
        asset = Asset(
            symbol      = request.form['symbol'],
            description = request.form['description'],
            type        = request.form['type'],
            exchange    = request.form['exchange'],
            size        = request.form['size'],
            coupon      = float(request.form['coupon']+'0'),
            strike      = int(request.form['strike']+'0'),
            expiry      = request.form['expiry'])
        logger.info('adding new asset: {}'.format({k:v for k,v in asset.__dict__.items() if type(v) in [str, float, int]}))
        session.add(asset)
        session.commit()
        return redirect(url_for('showAssets'))
    else:
        return render_template('newAsset.html', sec_types = RefData.secType, exchanges = RefData.exchange)

@app.route('/assets/<int:asset_id>/edit/', methods = ['GET', 'POST'])
def editAsset(asset_id):
    '''edit asset'''
    if request.method == 'POST':
        asset = assets.filter_by(id = asset_id).one()
        asset.symbol        = request.form['symbol']
        asset.description   = request.form['description']
        asset.type          = request.form['type']
        asset.exchange      = request.form['exchange']
        asset.size          = request.form['size']
        asset.coupon        = float(request.form['coupon']+'0')
        asset.strike        = int(request.form['strike']+'0')
        asset.expiry        = request.form['expiry']
        logger.info('updating asset: {}'.format({k:v for k,v in asset.__dict__.items() if type(v) in [str, float, int]}))
        session.add(asset)
        session.commit()
        return redirect(url_for('showAssets'))
    else:
        return render_template('editAsset.html', asset = assets.filter_by(id = asset_id).one(), sec_types = RefData.secType, exchanges = RefData.exchange)
    return "page to edit asset"

@app.route('/allocations/new/', methods = ['GET', 'POST'])
def newAllocation():
    '''add new allocation'''
    if request.method == 'POST':
        asset           = assets.filter_by(symbol = request.form['symbol']).one()
        allocation = Allocation(
            date_mod    = request.form['date_mod'],
            portfolio   = request.form['portfolio'],
            asset_id    = asset.id,
            allocation  = request.form['allocation'])
        logger.info('adding new allocation: {}'.format({k:v for k,v in allocation.__dict__.items() if type(v) in [str, float, int]}))
        session.add(allocation)
        session.commit()
        return redirect(url_for('showAllocations'))
    else:
        return render_template('newAllocation.html', assets = assets)

@app.route('/allocations/<int:allocation_id>/edit/', methods = ['GET', 'POST'])
def editAllocation(allocation_id):
    '''edit allocation'''
    if request.method == 'POST':
        allocation = allocations.filter_by(id = allocation_id).one()
        allocation.date_mod     = request.form['date_mod']
        allocation.portfolio    = request.form['portfolio']
        allocation.asset_id     = request.form['asset_id']
        allocation.allocation   = request.form['allocation']
        logger.info('updating allocation: {}'.format({k:v for k,v in allocation.__dict__.items() if type(v) in [str, float, int]}))
        session.add(allocation)
        session.commit()
        return redirect(url_for('showAllocations'))
    else:
        return render_template('editAllocation.html', allocation = allocations.filter_by(id = allocation_id).one(), assets = assets)


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

## ==========
## == main ==
## ==========

def main():
    app.jinja_env.globals.update(util=util)         # register util module with webserver to implement custom functions within a template
    app.debug == args.debug
    app.run(host = args.host, port = args.port)

## ============
## == module ==
## ============

if args.start   == True:
    main()
else:               # when running in interactive mode
    currentAllocations      = list(session.query(Asset.symbol, Allocation.allocation, Allocation.date_mod).join(Allocation))
    allocationsDF           = pd.DataFrame(currentAllocations)
    allocationsDF.date_mod  = pd.to_datetime(allocationsDF['date_mod'])
