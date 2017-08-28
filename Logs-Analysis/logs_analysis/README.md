# Project: Logs Analysis

### Install
This project is written in **Python 2.7**.

This project requires a database hosted on a Linux virtual machine -- follow the instructions 
found in part 3 of the Logs Analysis Project ("Prepare the software and data").

Once that is complete, unpack this folder into the `vagrant` directory, 
move into this folder and execute the command `psql -d news -f projectviews.sql`. 
This will set up three database views encapsulating the three queries required for the project.

### Code

All code needed to run this project is found in this directory.  Note that a design decision 
was made to host the query logic in the database layer (via views) rather than in the 
application layer; this type of design can sometimes be easier to maintain and optimize from a DB
perspective, at the cost of additional database objects and some opacity in the application layer.

### Run

From a command line prompt, move to the logs_analysis directory and run the python code 
found in `project.py`; the command is `python project.py`.  

Output for the project will be sent to standard output. Sample output can be found in `output.txt`.

### Data

All data required to run this project is loaded as part of the installation process above. 

View definitions can be found in the SQL script `projectviews.sql`.
