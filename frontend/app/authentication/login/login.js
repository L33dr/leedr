'use strict';

angular.module('myApp.login', ['ngRoute'])

.controller('LoginCtrl', ['$scope', '$rootScope', 'AUTH_EVENTS', 'AuthService', '$location', 'Session',
        function($scope, $rootScope, AUTH_EVENTS, AuthService, $location, Session) {
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
            $rootScope.loginInProcess = true;
          AuthService.login(credentials).then(function () {
              $rootScope.$broadcast(AUTH_EVENTS.loginSuccess);
              $rootScope.loginInProcess = false;
              $location.path('/dashboard');
              toastr.success("You logged in successfully.");
              $scope.closePopOuts();
              $scope.resetLoginField();
          }, function(data) {
              $rootScope.$broadcast(AUTH_EVENTS.loginFailed);
              $rootScope.loginInProcess = false;
              toastr.error(data.data.non_field_errors[0]);
              $scope.resetLoginField();
          });
        };
}]);