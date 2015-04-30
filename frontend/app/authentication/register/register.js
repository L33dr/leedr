'use strict';

angular.module('myApp.register', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/register', {
    templateUrl: 'authentication/register/register.html',
    controller: 'RegisterCtrl'
  });
}])

.controller('RegisterCtrl', ['$scope', 'Restangular', function($scope, Restangular) {
        // Submits the registration to the backend. If successful it will redirect to home page.
        // They will need to confirm email before they are able to sign in.
        $scope.submit = function () {
            Restangular.one('rest-auth/registration').customPOST($scope.user).then(function (){
                $scope.success = true;
                // TODO: Toastr message letting the user know they need to confirm their email.
                // TODO: Toastr success message.
            }, function() {
                $scope.success = false;
                // TODO: Toastr failure message
            });
        };
}]);