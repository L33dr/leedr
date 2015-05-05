'use strict';

angular.module('myApp.login', ['ngRoute'])

.controller('LoginCtrl', ['$scope', '$rootScope', 'AUTH_EVENTS', 'AuthService', '$location', function($scope, $rootScope, AUTH_EVENTS, AuthService, $location) {
        // Initializes the credential fields
        $scope.resetLoginField = function () {
            $scope.credentials = {
                username: '',
                password: ''
            };
        };

        $scope.resetLoginField();

        $scope.submit = function (credentials) {

            // Calls the login function, passing the credentials.
            // On success it will broadcast the login success event
            // set the current user then redirect to home page.
          AuthService.login(credentials).then(function (user) {
              $rootScope.$broadcast(AUTH_EVENTS.loginSuccess);
              $scope.setCurrentUser(user);
              $location.path('/');
              toastr.success("You logged in successfully.");
              $scope.closePopOuts();
              $scope.resetLoginField();
          }, function(data) {
              $rootScope.$broadcast(AUTH_EVENTS.loginFailed);
              toastr.error(data.data.non_field_errors[0]);
              $scope.resetLoginField();
          });
        };
}]);