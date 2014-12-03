'use strict';

function s3_upload(status_elem, url_elem, preview_elem){
  var s3upload = new S3Upload({
      file_dom_selector: 'files',
      s3_sign_put_url: '/sign_s3/',
      onProgress: function(percent, message) {
          status_elem.innerHTML = 'Upload progress: ' + percent + '% ' + message;
      },
      onFinishS3Put: function(url) {
          status_elem.innerHTML = 'Upload completed. Uploaded to: '+ url;
          url_elem.value = url;
          preview_elem.innerHTML = '<img src="'+url+'" style="width:300px;" />';
      },
      onError: function(status) {
          status_elem.innerHTML = 'Upload error: ' + status;
      }
  });
}

angular.module('prandiusApp.add_photo', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/add_photo', {
    templateUrl: 'add_photo/view2.html',
    controller: 'View2Ctrl'
  });
}])

.controller('View2Ctrl', ['$scope', '$http',
  function($scope, $http) {
    $scope.upload_succeeded = false;
    $scope.post_succeeded = false;
    $scope.logged_in = false;
    $http.get('/api/user_login_status/').success(function(data) {
      $scope.username_i = data["username"];
      $scope.name = data["name"];
      $scope.logged_in = data["logged_in"];
    });
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
          $scope.post_succeeded = true;
        }
      });
    }
    $scope.uploadPhoto = function(){
      console.log("Upload initiated");
      var status_elem = $("#status")[0];
      var url_elem = $("#photo_url")[0];
      var preview_elem = $("#preview")[0];
      s3_upload(status_elem, url_elem, preview_elem);
    }
    
  }
]);
