
'use strict';

(function() {
    angular.module('fireStation.homeController', [])

    .controller('home', function($scope, map, $filter, shelterServ) {
      var homeMap = map.initMap('map', {scrollWheelZoom: false});
        homeMap.setView([40, -90], 4);

        shelterServ.getAllShelters(function() {
          // Got all Shelters
          if (shelterServ.getShelters()) {
            var newGeoJSON = shelterServ.getGeoJSONFromShelters();
          }

          L.geoJson(newGeoJSON, {
            pointToLayer: function(feature, latlng) {
              // Don't use icon, gets default
              return L.marker(latlng, {});
            },
            onEachFeature: function(feature, layer) {
              var popUp = '<div><span style="padding-right: 5px;">' + feature.properties.name + '</span><a class="fa fa-chevron-right trigger" href=' + feature.properties.url + '></a></div>';
              layer.bindPopup(popUp);
            }
          }).addTo(homeMap);
        });
    });
})();

