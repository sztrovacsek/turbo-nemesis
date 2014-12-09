'use strict';

// Declare app level module which depends on views, and components
var prandiusApp = angular.module('prandiusApp', [
  'ngRoute',
  'prandiusApp.main_feed',
  'prandiusApp.map_feed',
  'prandiusApp.add_photo',
  'prandiusApp.post_page',
])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.otherwise({redirectTo: '/main_feed'});
}])

.controller('IndexCtrl', ['$scope', '$http',
  function($scope, $http) {
    $scope.todo_text = "todo";
    $http.get('/api/user_login_status/').success(function(data) {
      $scope.name = data["name"];
      $scope.logged_in = data["logged_in"];
    });
    $http.get('/api/csrf_token/').success(function(data) {
      console.log("Can login");
    });
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
    });

  }
])

;
