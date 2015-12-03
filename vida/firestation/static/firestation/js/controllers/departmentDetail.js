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

      .controller('personController', function($scope, $rootScope, $http, shelterServ) {
        $scope.shelterList = [];
        $scope.current_shelter = {};

        $scope.getShelterByUUID = function(id) {
          var shelter = shelterServ.getShelterByUUID(id);
          if (shelter) {
            document.getElementById("shelterID").innerHTML = '<div class="ct-u-displayTableCell">' +
              '<span class="ct-fw-600">Current Shelter</span></div>' +
              '<div class="ct-u-displayTableCell text-right">' +
              '<span>' + shelter.name + '   </span>' +
              '<a style="display: inline-block;"' +
              'class="fa fa-chevron-right trigger" href="/shelters/' + shelter.id + '\/" ></a></div> </div>';
            return shelter;
          } else
            return undefined;
        };

        $scope.getAllShelters = function() {
          shelterServ.getAllShelters(function() {});
        };

        $scope.getAllShelters();
      })
})();
