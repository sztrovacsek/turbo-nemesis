'use strict';

angular.module('prandiusApp.post_page', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/post_page/:postId', {
    templateUrl: 'post_page/view.html',
    controller: 'ViewCtrl'
  });
}])

.controller('ViewCtrl', ['$scope', '$routeParams', '$http',
  function($scope, $routeParams, $http) {
    $scope.todo_text = "todo";
    $http.get('/api/post_detail/'+$routeParams.postId+'/').success(function(data) {
      $scope.post = data;
      $scope.post.create_date = moment($scope.post.create_date).fromNow();
    });
  }
]);
