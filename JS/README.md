# Project: Neighborhood Map

This project displays locations that are sites for academic bowl tournaments
that Elkins Pointe Middle School will be competing in this year (the author is
the parent-coach for the team).  

### Install

This project requires an HTML5 compliant browser that supports JS (such as Chrome).  
A browser with integrated developer tools (such as Chrome) will 
facilitate examining the responsive design portions of the project.

The project makes use of JQuery 1.11.1 and Knockout 3.2.0, both of which are supplied in the `js\lib`
directory.  JQuery is not used to manipulate DOM elements, but rather for its param and getJSON methods.

### Code

All code needed to run this project is found in this directory.

### Run

Open the index.html file in an HTML5 compliant browser.
On a Windows system, you can easily do this by right-clicking on the file
and selecting "Open with...", and then selecting your preferred browser.

### Data

All data used by the project is static data found in the `data.js` file.  

### Review Notes
* Photographs are downloaded using the Foursquare API.  Clicking on the photo will open
a new window to the Foursquare site for the venue, per Foursquare attribution requirements.
* Filtering occurs real-time as the user types in the filter box.  Filtering is case-sensitive.
* Besides the required locations, an additional marker is provided for the location
of Elkins Pointe Middle School, to allow the location of the tournaments relative to the
school to be placed in context; this marker is labeled with an 'E' and is not subject to
filtering.
