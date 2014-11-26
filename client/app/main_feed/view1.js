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
    $http.get('/api/user_data/').success(function(data) {
      $scope.username = data["username"];
    });
    $scope.todo_text = "todo";
  }
]);
