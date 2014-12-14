'use strict';

angular.module('prandiusApp.map_feed', [
  'ngRoute',
  'uiGmapgoogle-maps'
])

.config(['$routeProvider', 'uiGmapGoogleMapApiProvider', function($routeProvider, uiGmapGoogleMapApiProvider){
  $routeProvider.when('/map_feed', {
    templateUrl: 'map_feed/view_map.html',
    controller: 'ViewMapCtrl'
  });
  uiGmapGoogleMapApiProvider.configure({
      key: 'AIzaSyAgPiMv21OmrvXbLHz6lnWfJLa_M1zqYnw',
      v: '3.18'
  });
}])

.controller('ViewMapCtrl', ['$scope', '$http', 'uiGmapGoogleMapApi',
  function($scope, $http, uiGmapGoogleMapApi) {
    console.log("map_feed controller: start");
    $http.get('/api/latest_posts/').success(function(data) {
      $scope.posts = data["posts"];
    });
    uiGmapGoogleMapApi.then(function(maps) {
      // temporary map position
      $scope.map = {
        center: {latitude: 51.508742, longitude: -0.120850},
        mapTypeId:google.maps.MapTypeId.ROADMAP,
        zoom: 10
      };

      // Try HTML5 geolocation
      if(navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
          var pos = new maps.LatLng(position.coords.latitude, position.coords.longitude);
          console.log("Pos: "+pos+"("+pos.k+","+pos.B+")");
          // real map position
          $scope.map.center = {latitude: pos.k, longitude: pos.B}

        }, function() {
          handleNoGeolocation(true);
        });
      } else {
        // Browser doesn't support Geolocation
        handleNoGeolocation(false);
      }

      function handleNoGeolocation(errorFlag) {
        if (errorFlag) {
          console.log('Error: The Geolocation service failed.');
        } else {
          console.log('Error: Your browser doesn\'t support geolocation.');
        }
      }
    }); // end: google map promise
  } // end: controller function
]);
