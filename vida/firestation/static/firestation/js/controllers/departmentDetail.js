'use strict';

(function() {
    angular.module('fireStation.departmentDetailController', [])

    .controller('jurisdictionController', function($scope, $http, FireStation, map, shelterServ) {
          var departmentMap = map.initMap('map', {scrollWheelZoom: false});
          var showStations = true;
          var stationIcon = L.VIDAMarkers.firestationmarker();
          var headquartersIcon = L.VIDAMarkers.headquartersmarker();
          var fitBoundsOptions = {};
          $scope.stations = [];
          var layersControl = L.control.layers().addTo(departmentMap);

          if (showStations) {
              FireStation.query({department: config.id}).$promise.then(function(data) {
                 $scope.stations = data.objects;

                  var stationMarkers = [];
                  var numFireStations = $scope.stations.length;
                  for (var i = 0; i < numFireStations; i++) {
                      var station = $scope.stations[i];
                      var marker = L.marker(station.geom.coordinates.reverse(), {icon: stationIcon});
                      marker.bindPopup('<b>' + station.name + '</b><br/>' + station.address + ', ' + station.city + ' ' +
                          station.state);
                      stationMarkers.push(marker);
                  }

				 if (numFireStations > 0) {
					var stationLayer = L.featureGroup(stationMarkers);
	
					// Uncomment to show Fire Stations by default
					// stationLayer.addTo(departmentMap);
	
					layersControl.addOverlay(stationLayer, 'Fire Stations');
	
					if (config.geom === null) {
						departmentMap.fitBounds(stationLayer.getBounds(), fitBoundsOptions);
					}
			     }
              });
          }

          if (config.centroid != null) {
           var headquarters = L.marker(config.centroid, {icon: headquartersIcon,zIndexOffset:1000});
           headquarters.addTo(departmentMap);
           layersControl.addOverlay(headquarters, 'Headquarters Location');
          };

          if (config.geom != null) {
           var countyBoundary = L.geoJson(config.geom, {
                                  style: function (feature) {
                                      return {color: '#0074D9', fillOpacity: .05, opacity:.8, weight:2};
                                  }
                              }).addTo(departmentMap);
            layersControl.addOverlay(countyBoundary, 'Jurisdiction Boundary');
            departmentMap.fitBounds(countyBoundary.getBounds(), fitBoundsOptions);
          } else {
              departmentMap.setView(config.centroid, 13);
          }

          $scope.toggleFullScreenMap = function() {
              departmentMap.toggleFullscreen();
          };

      })

    .controller('personController', function($scope, $rootScope, $http, shelterServ, personServ) {
        $scope.shelterList = [];
        $scope.current_shelter = {};
            $scope.personHistory = [];

        $scope.checkShelterByUUID = function(shelter_uuid, person_uuid) {
          var shelter = shelterServ.getShelterByUUID(shelter_uuid);
          var person = personServ.getPersonByUUID(person_uuid);

          if (shelter) {
            document.getElementById("shelterID").innerHTML = '<div class="ct-u-displayTableCell">' +
              '<span class="ct-fw-600">Current Location</span></div>' +
              '<div class="ct-u-displayTableCell text-right">' +
                // Show Shelter Name
              '<span>' + shelter.name + '   </span>' +
                // Show Link to Shelter
              '<a style="display: inline-block;"' +
              'class="fa fa-chevron-right trigger" href="/shelters/' + shelter.id + '\/" ></a></div> </div>';
            return shelter;
          } else {
            if (person) {
              // Check if person has Geometry
              if (person.geom) {

                var split_geom = person.geom.split('(')[1].split(')')[0].split(' ');
                var personLocation = {};
                personLocation.long = split_geom[0];
                personLocation.lat = split_geom[1];

                // Is there a Geom to display?
                var hasGeom_NotZero = true;

                // if both are 0.000, there is no Geom
                var lat = Number(Number(personLocation.lat).toFixed(3));
                var long = Number(Number(personLocation.long).toFixed(3));
                if (lat === 0.000 && long === 0.000)
                  hasGeom_NotZero = false;

                if (hasGeom_NotZero) {
                  document.getElementById("shelterID").innerHTML = '<div class="ct-u-displayTableCell">' +
                    '<span class="ct-fw-600">Current Location</span></div>' +
                    '<div class="ct-u-displayTableCell text-right"><span>' +

                      // Show Geom Data
                    '<b>Long:</b> ' + Number(personLocation.long).toFixed(5) + '<br>' +
                    '<b>Lat:</b> ' + Number(personLocation.lat).toFixed(5) + '</span>';

                  return person.geom;
                } else
                  return undefined;
              } else
               return undefined;
            } else
              return undefined;
          }
        };

        $scope.getAllShelters = function() {
          shelterServ.getAllShelters(function() {});
        };

        $scope.getAllPeople = function() {
          personServ.getAllPeople(function() {});
        };

        $scope.getAllShelters();
        $scope.getAllPeople();
    })
})();
