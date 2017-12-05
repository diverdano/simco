# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

# Summary
This Repository includes files for SIMCO, the Secret Investment Management Company
The purpose is to demonstrate capability for basic functionality for the investment firm.

* ability to view, add and update assets with common and type specific properties
* ability to view, add and update portfolio allocations
* ability to filter allocations for a given date and number of days forward
* ability to specify and calculate average allocation per symbol for given date range

# Version 1.0

* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)
This version attempts to adhere to a MVC design pattern separating the data model from the view and from the controller.

### How do I get set up? ###
1. clone repository on deployment environment
2. create sqlite database with sql script: `sqlite3 -init create_db.sql simco.db`
3. run webserver with port and debug options as desired: `python project.py --start --port=8000 --debug`
4. point browser to ip address and port (e.g.: `http://localhost:8000/`), base url "/" will redirect to assets page, navigation links allow testing of all functionality

# Setup
for this project I am using:

* os x 10.10.4	development environment, will confirm deployment on ec2/linux ami with python 3.x
* python 3.5	backend code
* sqlite3		database
* sqlalchemy	object/relational map, schema design 
* flask/tornado	basic webserver/html templates
* bootstrap		basic web widgets/UI components (minimal use for dynamic forms)
* aws/ec2		server instance/env

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact