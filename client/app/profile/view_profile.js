'use strict';

angular.module('prandiusApp.profile_page', [
  'ngRoute',
  'uiGmapgoogle-maps'
])

.config(['$routeProvider', 'uiGmapGoogleMapApiProvider', function($routeProvider, uiGmapGoogleMapApiProvider) {
  $routeProvider.when('/profile', {
    templateUrl: 'profile/view_profile.html',
    controller: 'ViewProfileCtrl'
  });
  uiGmapGoogleMapApiProvider.configure({
      key: 'AIzaSyAgPiMv21OmrvXbLHz6lnWfJLa_M1zqYnw',
      v: '3.18'
  });
}])

.controller('ViewProfileCtrl', ['$scope', '$routeParams', '$http', 'uiGmapGoogleMapApi',
  function($scope, $routeParams, $http, uiGmapGoogleMapApi) {
    console.log("profile_page controller: start");
    $http.get('/api/currentuser/latest_posts/').success(function(data) {
      $scope.posts = data["posts"];
      $scope.count = data["count"];
      $.map($scope.posts, function(value){
          value.create_date = moment(value.create_date).fromNow();
        });
    });
    $scope.clickSave = function(post) {
      var post_id = post.post_id;
      var description = post.description;
      var address = post.address_raw;
      console.log("Saving... "+post_id);
      uiGmapGoogleMapApi.then(function(maps) {
        var geocoder = new maps.Geocoder();
        geocoder.geocode( { 'address': address}, function(results, status) {
          var coords;
          if (status == google.maps.GeocoderStatus.OK) {
            coords = results[0].geometry.location; // google.maps.LatLng
            console.log(coords+" ("+coords.lat()+","+coords.lng()+" )");
          }
          else {
            console.log('Geocode was not successful for the following reason: ' + status);
          }
          $.ajax({
            url: "/api/post_edit/",
            headers: {'X-CSRFToken': $.cookie('csrftoken')},
            data: {"post_id": post_id, "description": description, "coords_x": coords.lat(), "coords_y": coords.lng(), "address_raw": address},
            type: "POST",
            dataType: "JSON",
            success: function(json){
              console.log("Post succeeded");
            }
          });
        });
      });
    }

    $scope.clickDelete = function(post_id) {
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
