'use strict';

angular.module('prandiusApp.main_feed', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/main_feed', {
    templateUrl: 'main_feed/view1.html',
    controller: 'View1Ctrl'
  });
}])

.controller('View1Ctrl', ['$scope', '$http', '$timeout',
  function($scope, $http, $timeout) {
    console.log("main_feed controller: start");
    $scope.todo_text = "todo";
    $http.get('/api/latest_posts/').success(function(data) {
      $scope.posts = data["posts"];
      $.map($scope.posts, function(value){
          value.create_date = moment(value.create_date).fromNow();
        });
    });
  }
])
.directive('btFbParse', function () {
  return {
    restrict:'A',
    link:function (scope, element, attrs) {
      console.log(scope.post.permalink_fb);
      if (typeof FB === "undefined"){
        console.log("FB undefined (still)");
      }
      else{
        console.log("running FB parse");
        FB.XFBML.parse();
      }
    }
};
 }
);
