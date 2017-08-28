// Javascript methods and variables to support the Google Map component
// of the application
var MAP = (function() {

	// Display components
	let map = null;
	let infoWindow = null;

	// An array for the location markers
	let markers = [];

	// Initialize the map and markers
	function initMap(data) {
		map = new google.maps.Map(
			document.getElementById('map'),
			{
				center: data.homeLocation.position,
				zoom: 13,
			}
		);

		const homeMarker = new google.maps.Marker({
			position: data.homeLocation.position,
			title: 'Elkins Pointe Middle School',
			animation: google.maps.Animation.DROP,
			id: -1,
			icon: "http://maps.google.com/mapfiles/markerE.png"
		});
		homeMarker.setMap(map);
		homeMarker.addListener('click', function() {
			updateSelectedMarker(this);
		});

		infoWindow = new google.maps.InfoWindow();

		const locations = data.locations;
		for (let i = 0; i < locations.length; i++) {
			addMarkerForLocation(locations[i]);
		}

		showAllLocationMarkers();
	}

	// Add marker for location
	function addMarkerForLocation(location) {
		const marker = new google.maps.Marker({
			position: location.position,
			title: location.title,
			animation: google.maps.Animation.DROP,
			id: location.id
		});

		markers.push(marker);

		// Create an onclick event to open an infowindow at each marker.
		marker.addListener('click', function() {
			updateSelectedMarker(this);
		});
	}

	//Helper function to build the title HTML consistently
	function buildInfowindowContent(title, content) {
		return '<div>' + title + '</div><div>' + content + '</div>';
	}

	// This function moves the infoWindow to the currently selected marker
	// and displays a Foursquare photograph
	function updateSelectedMarker(marker) {
	// Check to make sure this marker is not already the current marker
		if (infoWindow.marker != marker) {
			if (infoWindow.marker != null) {
				infoWindow.marker.setAnimation(null);
			}
			infoWindow.marker = marker;
			infoWindow.marker.setAnimation(google.maps.Animation.BOUNCE);
			infoWindow.setContent(buildInfowindowContent(marker.title, ''));

			lookupFoursquarePhoto(marker.title, marker.position);

			infoWindow.open(map, marker);

			// Make sure the marker property is cleared if the infowindow is closed.
			infoWindow.addListener('closeclick', function() {
				if (infoWindow.marker != null) {
					infoWindow.marker.setAnimation(null);
					infoWindow.marker = null;
				}
			});
		}
	}

	// Loop through the markers array and display them all.
	function showAllLocationMarkers() {
		const bounds = new google.maps.LatLngBounds();
		// Extend the boundaries of the map for each marker and display the marker
		for (let i = 0; i < markers.length; i++) {
			markers[i].setMap(map);
			bounds.extend(markers[i].position);
		}
		map.fitBounds(bounds);
	}

	// Display only the markers corresponding to the provided locations
	function filterLocationMarkers(locations) {
		const locationIDs = locations.map(function(location) {return location.id;});
		for (let i = 0; i < markers.length; i++) {
			if (locationIDs.includes(markers[i].id)) {
				markers[i].setVisible(true);
			}
			else {
				markers[i].setVisible(false);
			}
		}
	}

//
// FOURSQUARE API CODE
//
	const foursquareClientID = "VO3JBRTA3JBXUZCYDGFDD3Z0DAP2AMDUHR1V5OILXMAT20P3";
	const foursquareClientSecret = "K2CL3MFWKEYBYOE3J5LPWQJTX0FDV3HQ3FFO1JD0VI1GFWUR";

	// Step 1 of retrieving the photo -- using the title and position, look up
	// the venue
	function lookupFoursquarePhoto(title, position) {
		let searchURL = 'https://api.foursquare.com/v2/venues/search';
    	searchURL += '?' + $.param({'client_id': foursquareClientID});
    	searchURL += '&' + $.param({'client_secret': foursquareClientSecret});
    	searchURL += '&' + $.param({'v': '20170817'});
    	searchURL += '&' + $.param({'ll': position.lat().toString() + ',' + position.lng().toString()});
    	searchURL += '&' + $.param({'query': title});
    	searchURL += '&' + $.param({'limit': 1});

		$.getJSON(searchURL, function(data) {
			venueID = data.response.venues[0].id;
			lookupFoursquarePhotoStep2(title, venueID);
		}).fail(function(e) {
			infoWindow.setContent(buildInfowindowContent(title, 'Error accessing Foursquare venue API'));
		});
	}

	// Step 2 of retrieving the photo -- look up the photos and put add the
	// first photo to the info window, along with Foursquare attribution
	function lookupFoursquarePhotoStep2(title, venueID)
	{
		let lookupURL = 'https://api.foursquare.com/v2/venues/' + venueID + '/photos';
    	lookupURL += '?' + $.param({'client_id': foursquareClientID});
    	lookupURL += '&' + $.param({'client_secret' : foursquareClientSecret});
    	lookupURL += '&' + $.param({'v': '20170817'});
    	lookupURL += '&' + $.param({'limit': 1});

    	const imageSize = '200x200';

		$.getJSON(lookupURL, function(data) {
			if (data.response.photos.items.length > 0) {
				const photo = data.response.photos.items[0];
				const photoURL = photo.prefix + imageSize + photo.suffix;

				let attributionURL = 'https://foursquare.com/v/' + venueID;
				attributionURL += '?' + $.param({'ref': foursquareClientID});

				let foursquareHTML = '<figure>';
				foursquareHTML += '<a href="' + attributionURL +'" target="_blank">';
				foursquareHTML += '<img src="' + photoURL + '"/>';
				foursquareHTML += '</a>';
				foursquareHTML += '<figcaption>Photo provided by Foursquare</figcaption>';
				foursquareHTML += '</figure>';
				infoWindow.setContent(buildInfowindowContent(title, foursquareHTML));
			}
			else {
				infoWindow.setContent(buildInfowindowContent(title, 'No photos found'));
			}
		}).fail(function(e) {
			infoWindow.setContent(buildInfowindowContent(title, 'Error accessing Foursquare photo API'));
		});
	}

	// Return the external methods beiong exposed outside the closure
	return {
		callbackInitMap: function() {
			initMap(DATA);
		},

		handleInitError: function() {
			alert("Google Map failed to load.");
		},

		selectMarker: function(location_id) {
			const marker = markers.filter(function(elem) {
				return elem.id == location_id;
			})[0];

			updateSelectedMarker(marker);
		},

		updateMarkers: function(locations) {
			filterLocationMarkers(locations);
		}
	};
})();
