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
    $scope.todo_text = "todo";
    console.log("map_feed controller: start");
    uiGmapGoogleMapApi.then(function(maps) {
      console.log("map can now be defined");
      //promise
      $scope.map = {
        center: {latitude: 45, longitude: -73},
        mapTypeId:google.maps.MapTypeId.ROADMAP,
        zoom: 8
      };
      console.log("map defined");
    });
  }
]);
