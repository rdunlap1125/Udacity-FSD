# Project: Build an Item Catalog

### Install

This project was built using Python 2.7 and the following additional packages (and any dependencies of those packages):
* Flask (0.2.12)
* Flask-SQLAlchemy (2.2)
* oauth2client (4.1.2)
* requests (2.18.4)
* SQLAlchemy (1.1.13)

A Vagrant configuration file is supplied that will download these libraries -- to make use of it, you wil need:
* A terminal program (on Windows, Git Bask is recommended)
* VirtualBox (https://www.virtualbox.org/wiki/Downloads)
* Vagrant (https://www.vagrantup.com/downloads.html)

To use Vagrant, navigate in your terminal program to the directory containing the file Vagrantfile (the top-level directory in 
the project) and run the command `vagrant up` to launch the VM.  Once it is up and running, run the command `vagrant ssh` to log in 
and get a Linux shell, then `cd /vagrant' to get to the top level directory.

This project also requires an HTML5 compliant browser (such as Chrome).

### Code

All code needed to run this project is found in the `catalog` directory.

### Data

To set up the database needed for this project, run the following commands:
* `python database_setup.py` -- this sets up the initial tables
* `python database_populate.py` -- this adds initial data to the tables.  

NOTE: If you wish to change the default owner of the initial items, edit line 14 of `database_populate.py` before running it.

### Run

In your terminal program, run the command `python project.py`.  Then, in a browser, open http://localhost:8000/catalog.

Without logging in, you can navigate through the catalog and view items.  After logging in,
new items can be added to a category on the category page, and items owned by a user can be added and
deleted from the item page.  Since the specification called for the actual names to be used in the URL,
a design decision was made to not allow the names of items to be edited -- only the descriptions can be altered,

The following JSON endpoints are also available -- each replicates the data available on the respective page:
* http://localhost:8000/catalog/JSON
* http://localhost:8000/catalog/<category-name>/items/JSON
* http://localhost:8000/catalog/<category-name>/<item-name>/JSON

### Review Notes
In three places, literal strings exceeding 80 characters cause PEP-8 errors (two of them are URLs).  Rather than
artifically break the strings up and reduce readability, I chose to leave them intact.



