'use strict';

angular.module('prandiusApp.map_feed', ['ngRoute', 'ui.map'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/map_feed', {
    templateUrl: 'map_feed/view.html',
    controller: 'ViewCtrl'
  });
}])

.controller('ViewCtrl', ['$scope', '$http',
  function($scope, $http) {
    $scope.todo_text = "todo";
    $scope.mapOptions = {
      center: new google.maps.LatLng(35.784, -78.670),
      zoom: 15,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };    
    
    // google maps stuff
    console.log("map_feed controller: start");
  }
]);
