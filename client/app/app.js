'use strict';

// Declare app level module which depends on views, and components
var prandiusApp = angular.module('prandiusApp', [
  'ngRoute',
  'prandiusApp.main_feed',
  'prandiusApp.map_feed',
  'prandiusApp.add_photo',
  'prandiusApp.post_page',
  'prandiusApp.profile_page',
])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.otherwise({redirectTo: '/main_feed'});
}])

.controller('IndexCtrl', ['$scope', '$http',
  function($scope, $http) {
    $scope.logged_in = false;
    $scope.todo_text = "todo";
    $http.get('/api/user_login_status/').success(function(data) {
      $scope.name = data["name"];
      $scope.logged_in = data["logged_in"];
    });
    $http.get('/api/csrf_token/').success(function(data) {
      console.log("Check");
    });

    $scope.login = function() {
      if ($scope.logged_in) { return; }
      console.log("Login starting...");
      FB.login(function(response){
        statusChangeCallback(response);
      }, {scope: 'public_profile,email,user_friends'});
    }

    $scope.logout = function() {
      if (!$scope.logged_in) { return; }
      console.log("Logout starting...");
      $.ajax({
        url: "/api/backend_logout/",
        headers: {'X-CSRFToken': $.cookie('csrftoken')},
        data: {},
        type: "POST",
        dataType: "JSON",
        success: function(json){
          console.log("Logout succeeded");
          $scope.logged_in = false;
        }
      });
    }
  }
])

;
