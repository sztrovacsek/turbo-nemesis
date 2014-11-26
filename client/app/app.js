'use strict';

// Declare app level module which depends on views, and components
var prandiusApp = angular.module('prandiusApp', [
  'ngRoute',
  'prandiusApp.main_feed',
  'prandiusApp.map_feed',
  'prandiusApp.add_photo',
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.otherwise({redirectTo: '/main_feed'});
}]);
