'use strict';

angular.module('myApp.confirmEmail', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/confirm-email/:key', {
    templateUrl: 'confirm-email/confirm-email.html',
    controller: 'ConfirmEmailCtrl'
  });
}])

.controller('ConfirmEmailCtrl', ['$scope', '$routeParams', 'Restangular', function($scope, $routeParams, Restangular) {
        $scope.submit = function () {
            $scope.key = { key: $routeParams.key };
            Restangular.one('rest-auth/registration/verify-email').customPOST($scope.key).then(function (message){
                $scope.message = message.message;
            }, function() {
            });
        };
}]);