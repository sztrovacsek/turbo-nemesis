'use strict';

angular.module('prandiusApp.view2', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/view2', {
    templateUrl: 'view2/view2.html',
    controller: 'View2Ctrl'
  });
}])

.controller('View2Ctrl', ['$scope', '$http',
  function($scope, $http) {
    $scope.savePhoto = function(){
      var photo_url = $('#avatar_url')[0].value;
      console.log(photo_url);
      console.log($scope.photo_url);
      // post the data to the server
      $.ajax({
        url: "/api/photo_add/",
        headers: {'X-CSRFToken': $.cookie('csrftoken')},
        data: photo_url,
        type: "POST",
        dataType: "JSON",
        success: function(json){
          console.log("Post succeeded");
        }
      });
    }
    
  }
]);
