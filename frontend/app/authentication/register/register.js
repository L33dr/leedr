'use strict';

angular.module('myApp.register', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/register', {
    //templateUrl: 'authentication/register/register.html',
    controller: 'RegisterCtrl'
  });
}])

.controller('RegisterCtrl', ['$scope', 'Restangular', function($scope, Restangular) {
        // Submits the registration to the backend. If successful it will redirect to home page.
        // They will need to confirm email before they are able to sign in.

        $scope.checked = false;

        $scope.toggle = function () {
            $scope.checked = !$scope.checked;
        };

        $scope.showSignup = false;

        $scope.toggleSignup = function () {
            $scope.showSignup = !$scope.showSignup;
        };

        $scope.submit = function () {
            Restangular.one('rest-auth/registration').customPOST($scope.user).then(function (){
                $scope.success = true;
                toastr.message("Please confirm your email.")
                toastr.success("Your profile was created successfully.")
            }, function() {
                $scope.success = false;
                toastr.error("There was a problem creating your account.")
            });
        };
}]);