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
      console.log($scope.photo_url);
      // post the data to the server
      $.ajax({
        url: "/api/photo_add/",
        headers: {'X-CSRFToken': $.cookie('csrftoken')},
        data: $scope.photo_url,
        type: "POST",
        dataType: "JSON",
        success: function(json){
          console.log("Post succeeded");
        }
      });
    }
    
  }
]);
