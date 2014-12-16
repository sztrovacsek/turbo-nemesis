'use strict';

angular.module('prandiusApp.profile_page', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/profile', {
    templateUrl: 'profile/view_profile.html',
    controller: 'ViewProfileCtrl'
  });
}])

.controller('ViewProfileCtrl', ['$scope', '$routeParams', '$http',
  function($scope, $routeParams, $http) {
    console.log("profile_page controller: start");
    $http.get('/api/currentuser/latest_posts/').success(function(data) {
      $scope.posts = data["posts"];
      $.map($scope.posts, function(value){
          value.create_date = moment(value.create_date).fromNow();
        });
    });
    if (typeof FB === "undefined"){
      console.log("FB undefined (still)");
    }
    else{
      FB.XFBML.parse();
    }
  }
]);
