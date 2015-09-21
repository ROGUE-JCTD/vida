(function () {
  "use strict";
  L.VIDAMarkers = {};

  L.VIDAMarkers.Icon = L.Icon.extend({
    options: {
      iconSize: [30,70],
      popupAnchor: [0,-30],
      shadowAnchor: null,
      shadowSize: null,
      shadowUrl: null
    }
  });

  L.VIDAMarkers.icon = function(options) {
    return new L.VIDAMarkers.Icon(options);
  };

  L.VIDAMarkers.firestationmarker = function(options) {
     var defaultOptions = {iconUrl:'/static/firestation/fire-station.png',
                           iconRetinaUrl: '/static/firestation/fire-station@2x.png'};
     return new L.VIDAMarkers.Icon(L.extend(defaultOptions, options));
  };

  L.VIDAMarkers.headquartersmarker = function(options) {
     var defaultOptions = {iconUrl:'/static/firestation/headquarters.png',
                           iconRetinaUrl: '/static/firestation/headquarters@2x.png'};
     return new L.VIDAMarkers.Icon(L.extend(defaultOptions, options));
  };

})();
