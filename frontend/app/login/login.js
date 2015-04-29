'use strict';

angular.module('myApp.login', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/login', {
    templateUrl: 'login/login.html',
    controller: 'LoginCtrl'
  });
}])

.controller('LoginCtrl', ['$scope', 'Restangular', function($scope, Restangular) {
        $scope.submit = function () {
            Restangular.one('rest-auth/login').customPOST($scope.user).then(function (){
                $scope.success = true;
            }, function() {
                $scope.success = false;
            });
        };
}]);