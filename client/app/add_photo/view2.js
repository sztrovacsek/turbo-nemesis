'use strict';

angular.module('prandiusApp.add_photo', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/add_photo', {
    templateUrl: 'add_photo/view2.html',
    controller: 'View2Ctrl'
  });
}])

.controller('View2Ctrl', ['$scope', '$http',
  function($scope, $http) {
    $scope.savePhoto = function(){
      var photo_url = $('#photo_url')[0].value;
      console.log(photo_url);
      var description = $('#description')[0].value;
      console.log(description);
      // post the data to the server
      $.ajax({
        url: "/api/photo_add/",
        headers: {'X-CSRFToken': $.cookie('csrftoken')},
        data: {"photo_url": photo_url, "description": description},
        type: "POST",
        dataType: "JSON",
        success: function(json){
          console.log("Post succeeded");
        }
      });
    }
    
  }
]);
