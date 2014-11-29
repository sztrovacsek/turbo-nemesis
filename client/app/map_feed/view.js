'use strict';

angular.module('prandiusApp.map_feed', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/map_feed', {
    templateUrl: 'map_feed/view.html',
    controller: 'ViewCtrl'
  });
}])

.controller('ViewCtrl', ['$scope', '$http',
  function($scope, $http) {
    $http.get('/api/user_data/').success(function(data) {
      $scope.username = data["username"];
      $scope.name = data["name"];
    });
    $scope.todo_text = "todo";
  }
]);
