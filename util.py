#!/usr/bin/env python

## ==================================
## === packages, modules, pragmas ===
## ==================================

## === built-ins ===
#import sys
from datetime   import date, timedelta, datetime
from time       import localtime, strftime, strptime, sleep, mktime
import logging
import logging.config                                       # pythons logging feature

## ===================================
## === logging to file and console ===
## ===================================

def setLogLevel(debug_level, log_file):
    ''' set logging debug level '''
    ERROR_FORMAT        = "%(asctime)s %(name)s %(levelname)-8s %(message)s"
    INFO_FORMAT         = "%(asctime)s %(name)s %(levelname)-8s %(message)s"
    CONSOLE_FORMAT      = "\t%(message)s"
    if debug_level == True:
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
                                      'filename':log_file,
                                      'formatter':'debug',
                                      'level':logging.INFO}},
                  'root':{'handlers':['console', 'file'], 'level':LOG_LEVEL}}
    logging.config.dictConfig(LOG_CONFIG)

## =========================
## === support functions ===
## =========================

def date2epoch(value, option=1):
    if int(option) == 1  : pattern = '%Y-%m-%d'
    elif int(option) == 2: pattern = '%Y-%m'
    elif int(option) == 3: pattern = '%Y-%m-%dT%H:%M:%SZ'
    elif int(option) == 4: pattern = '%Y-%m-%d %H:%M:%S'
    elif int(option) == 5: pattern = '%m/%d/%Y'
    return int(mktime(strptime(value, pattern)))

def epoch2date(value, option=1):
    if int(option) == 1  : pattern = '%Y-%m-%d'
    elif int(option) == 2: pattern = '%Y-%m'
    elif int(option) == 3: pattern = '%Y-%m-%dT%H:%M:%SZ'
    elif int(option) == 4: pattern = '%Y-%m-%d %H:%M:%S'
    elif int(option) == 5: pattern = '%m/%d/%Y'
    return (strftime(pattern, localtime(value)))

def displayTime(value=None, offset=0, option=1, strip_option=1):
    ''' date passed as string '''
    offset = int(offset)
    if value == None: d = (date.today() + timedelta(offset))
    else:
        start_date  = date2epoch(value, option=strip_option)
        end_date    = start_date + offset * 86400
        d           = localtime(end_date)
    if   option == 1: return strftime('%Y-%m-%d', d)
    elif option == 2: return strftime('%Y-%m-%d %H:%M:%S', d)
    elif option == 3: return strftime('%H:%M:%S', d)
    elif option == 4: return strftime('%Y-%m-%d %H:%M', d)
    elif option == 5: return strftime('%Y%m%d', d)
    elif option == 6: return strftime('%Y%m%dT%H:%M', d)
    elif option == 7: return strftime('%Y-%m-%dT%H:%M', d)
    else            : return strftime('%s', d)

def pickDate(offset=0, show_date=True):
    offset = int(offset)
    now = datetime.now()+timedelta(offset)
    day = datetime(now.year, now.month, now.day)
    if show_date ==True: print(logger('Status') + 'datestamp applied: ' + day.strftime("%Y-%m-%d"))
    return day.strftime("%Y-%m-%d")
