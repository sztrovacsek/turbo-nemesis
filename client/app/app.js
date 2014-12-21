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

    // This is called with the results from from FB.getLoginStatus().
    function statusChangeCallback(response) {
      console.log('statusChangeCallback');
      console.log(response);
      if (response.status === 'connected') {
        // Logged into your app and Facebook.
        fbLoginConfirmed(response);
      } else if (response.status === 'not_authorized') {
        // The person is logged into Facebook, but not your app.
      } else {
        // The person is not logged into Facebook, so we're not sure if
        // they are logged into this app or not.
      }
    }

    // login flow, final step
    function fbLoginConfirmed(response) {
      var uid = response.authResponse.userID;
      var accessToken = response.authResponse.accessToken;
      console.log('Welcome!  Fetching your information.... ');
      FB.api('/me', function(response) {
        console.log('Successful login for: ' + response.name);
        loginBackend(uid, accessToken, response);
      });
    }

    // login to the prandius backend
    function loginBackend(uid, accessToken, fbData){
      var csrf = $.cookie('csrftoken');
      console.log("Backend login: start");
      $.ajax({
        url: "/api/backend_login/",
        headers: {
          'X-CSRFToken': $.cookie('csrftoken'),
        },
        data: {"fbUid": uid, "fbData": fbData, "name": fbData.name, "accessToken": accessToken, 'X-CSRFToken': $.cookie('csrftoken')},
        type: "POST",
        dataType: "JSON",
        success: function(json){
          console.log("Backend login: post succeeded");
          // redirect (todo: replace this with scope apply)
          location.href = "index.html";
        }
      });
    }

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
          // redirect (todo: replace this with scope apply)
          location.href = "index.html";
        }
      });
    }
  }
])

;
