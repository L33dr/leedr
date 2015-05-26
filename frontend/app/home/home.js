'use strict';

angular.module('myApp.home', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/home', {
    templateUrl: 'home/home.html',
    controller: 'HomeCtrl'
  });
}])

.controller('HomeCtrl', ['$scope', 'Restangular', 'gameService', function($scope, Restangular, gameService) {
        $scope.comment = {};
        $scope.games = gameService;
        $scope.submit = function() {
            Restangular.all("leedr/comment").customPOST($scope.comment).then(function () {
                    toastr.success("Your comment was successfully submitted.");
                    $scope.comment = {};
                }, function (data) {
                    toastr.error("There was a problem submitting your comment.");
                }
            )
        }
}]);