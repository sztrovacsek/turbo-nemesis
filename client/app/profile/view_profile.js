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
      $scope.count = data["count"];
      $.map($scope.posts, function(value){
          value.create_date = moment(value.create_date).fromNow();
        });
    });
    $scope.clickSave = function(post_id, description){
      console.log("Saving... "+post_id);
      $.ajax({
        url: "/api/post_edit/",
        headers: {'X-CSRFToken': $.cookie('csrftoken')},
        data: {"post_id": post_id, "description": description},
        type: "POST",
        dataType: "JSON",
        success: function(json){
          console.log("Post succeeded");
        }
      });
    }

    $scope.clickDelete = function(post_id){
      console.log("Deleting... "+post_id);
      $.ajax({
        url: "/api/post_delete/",
        headers: {'X-CSRFToken': $.cookie('csrftoken')},
        data: {"post_id": post_id},
        type: "POST",
        dataType: "JSON",
        success: function(json){
          console.log("Post succeeded");
          var posts = $scope.posts.filter(function(post){ return (post.post_id != post_id)});
          $scope.posts = posts;
          // TODO: call: $scope.$digest(); or something
        }
      });
    }

    if (typeof FB === "undefined"){
      console.log("FB undefined (still)");
    }
    else{
      FB.XFBML.parse();
    }
  }
]);
