'use strict';

angular.module('prandiusApp.main_feed', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/main_feed', {
    templateUrl: 'main_feed/view1.html',
    controller: 'View1Ctrl'
  });
}])

.controller('View1Ctrl', ['$scope', '$http',
  function($scope, $http) {
    $scope.todo_text = "todo";
    $http.get('/api/latest_posts/').success(function(data) {
      $scope.posts = data["posts"];
      $.map($scope.posts, function(value){
          value.create_date = moment(value.create_date).fromNow();
        });
    });
    FB.XFBML.parse();
  }
]);
