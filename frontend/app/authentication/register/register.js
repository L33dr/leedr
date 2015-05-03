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

        $scope.showSignup = false;

        $scope.toggleSignup = function () {
            $scope.showSignup = !$scope.showSignup;
        };

        $scope.submit = function () {
            Restangular.one('rest-auth/registration').customPOST($scope.user).then(function (){
                $scope.success = true;
                $scope.user = null;
                $scope.showSignup = !$scope.showSignup;
                toastr.info("Please confirm your email.")
                toastr.success("Your profile was created successfully.")
            }, function() {
                $scope.success = false;
                toastr.error("There was a problem creating your account.")
            });
        };
}]);