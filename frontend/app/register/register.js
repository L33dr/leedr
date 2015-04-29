'use strict';

angular.module('myApp.register', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/register', {
    templateUrl: 'register/register.html',
    controller: 'RegisterCtrl'
  });
}])

.controller('RegisterCtrl', ['$scope', 'Restangular', function($scope, Restangular) {
        $scope.submit = function () {
            Restangular.one('rest-auth/registration').customPOST($scope.user).then(function (){
                $scope.success = true;
            }, function() {
                $scope.success = false;
            });
        };
}]);