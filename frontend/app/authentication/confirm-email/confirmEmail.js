'use strict';

angular.module('myApp.confirmEmail', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/confirm-email/:key', {
    templateUrl: 'authentication/confirm-email/confirm-email.html',
    controller: 'ConfirmEmailCtrl'
  });
}])

.controller('ConfirmEmailCtrl', ['$scope', '$routeParams', 'Restangular', '$location', function($scope, $routeParams, Restangular, $location) {
        $scope.submit = function () {

            // Gets key from URL
            $scope.key = { key: $routeParams.key };
            // Posts that key to the backend confirming the email address.
            Restangular.one('rest-auth/registration/verify-email').customPOST($scope.key).then(function (){
                // Redirect to home page.
                $location.path('/');
                toastr.success("You're email has successfully been verified.")
            }, function() {
                toastr.error("There was a problem verifying your email.")
            });
        };
}]);