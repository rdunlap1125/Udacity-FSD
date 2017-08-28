var KNOCKOUTVM = function() {
	var Location = function(location) {
		this.title = ko.observable(location.title);
		this.id = ko.observable(location.id);
	};

	var ViewModel = function() {
		const self = this;

		this.locationList = ko.observableArray([]);

		this.filterString = ko.observable("");
		this.filterString.subscribe(function() {
			self.filterChanged();
		});

		DATA.locations.forEach(function(location) {
			self.locationList.push(new Location(location));
		});

		this.selectLocation = function(location) {
			MAP.selectMarker(location.id());
		};

		this.filterChanged = function() {
			filter = self.filterString().trim();
			let matchingLocations = [];
			if (filter == "") {
				matchingLocations = DATA.locations;
			}
			else {
				matchingLocations = DATA.locations.filter(function(location) {
					return location.title.match(self.filterString()) != null;
				});
			}

			//Update the Knockout observables
			self.locationList([]);

			matchingLocations.forEach(function(location) {
				self.locationList.push(new Location(location));
			});

			//Send the location list to the map to update visible markers
			MAP.updateMarkers(matchingLocations);
		};

		this.selectorsVisible = ko.observable(true);
		this.toggleSelectors = function() {
			self.selectorsVisible(!self.selectorsVisible());
		};
	};

	// Return the external methods beiong exposed outside the closure
	return {
		initializeBindings: function() {
			ko.applyBindings(new ViewModel());
		}
	};
}();

KNOCKOUTVM.initializeBindings();