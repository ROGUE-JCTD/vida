/**
 * Created by s30577 on 4/21/16.
 */
'use strict';

(function() {
    angular.module('fireStation.personService', [])

   .service('personServ', function($http, $resource){
        var people = [];

        this.getAllPeople = function(success) {
          var person_promise = $resource('/api/v1/person/', {}, {
            query: {
              method: 'GET',
              isArray: true,
              transformResponse: $http.defaults.transformResponse.concat([
                function (data, headersGetter) {
                  people = data.objects;
                  success();
                }
              ])
            }
          });
          return person_promise.query().$promise;
        };

        this.getPeople = function() {
          return people;
        };

        this.getPersonByUUID = function(id) {
          for (var i = 0; i < people.length; i++){
            if (people[i].uuid === id){
              return people[i];
            }
          }

          return undefined;
        };
      })
})();
