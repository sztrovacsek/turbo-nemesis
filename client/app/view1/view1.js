'use strict';

angular.module('prandiusApp.view1', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/view1', {
    templateUrl: 'view1/view1.html',
    controller: 'View1Ctrl'
  });
}])

.controller('View1Ctrl', ['$scope', '$http',
  function($scope, $http) {
    $http.get('/api/user_data/').success(function(data) {
      $scope.username = data["username"];
    });
    $scope.todo_text = "todo";
  }
]);
