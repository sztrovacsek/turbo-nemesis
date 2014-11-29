'use strict';

// Declare app level module which depends on views, and components
var prandiusApp = angular.module('prandiusApp', [
  'ngRoute',
  'prandiusApp.main_feed',
  'prandiusApp.map_feed',
  'prandiusApp.add_photo',
])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.otherwise({redirectTo: '/main_feed'});
}])

.controller('IndexCtrl', ['$scope', '$http',
  function($scope, $http) {
    $scope.todo_text = "todo";
    $http.get('/api/user_login_status/').success(function(data) {
      $scope.username_i = data["username"];
      $scope.name = data["name"];
      $scope.logged_in = data["logged_in"];
    });
  }
])

;
