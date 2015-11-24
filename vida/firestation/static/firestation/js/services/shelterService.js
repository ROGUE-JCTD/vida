'use strict';

(function() {
    angular.module('fireStation.shelterService', [])

    .service('shelterServ', function($http, $resource){
        var shelters = [];

        this.getAllShelters = function(success) {
          var shelter = $resource('/api/v1/shelter/', {}, {
            query: {
              method: 'GET',
              isArray: true,
              transformResponse: $http.defaults.transformResponse.concat([
                function (data, headersGetter) {
                  shelters = data.objects;
                  console.log('----[ transformResponse data: ', data);
                  success();
                }
              ])
            }
          });
          return shelter.query().$promise;
        };

        this.getShelters = function() {
          return shelters;
        };

        this.getGeoJSONFromShelters = function() {
          var newGeoJSON = "{" +
              "\"type\":\"FeatureCollection\"," +
              "\"totalFeatures\":" + shelters.length + "," +
              "\"features\":[";

            for (var i = 0; i < shelters.length; i++){
              var latLng = this.getLatLng(shelters[i]);
              newGeoJSON += "{\"type\":\"Feature\"," +
                            "\"geometry\":{ \"type\":\"Point\"," +
                            "\"coordinates\":[" + latLng.lng + "," + latLng.lat + "]}," +
                            "\"geometry_name\":\"geom\"," +
                            "\"properties\":{ " +
                              "\"name\":\"" + shelters[i].name + "\"," +
                              "\"url\":\"" + '/shelters/' + shelters[i].id + "\"}}";

              if (i !== shelters.length - 1)
                newGeoJSON += ",";
            }

            newGeoJSON += "]}";

            return JSON.parse(newGeoJSON);
        };

        this.getLatLng = function(shelter) {
          var trimParens = /^\s*\(?(.*?)\)?\s*$/;
          var coordinateString = shelter.geom.toLowerCase().split('point')[1].replace(trimParens, '$1').trim();
          var tokens = coordinateString.split(' ');
          var lng = parseFloat(tokens[0]);
          var lat = parseFloat(tokens[1]);
          return {lat: lat, lng: lng};
        };
      })
})();
