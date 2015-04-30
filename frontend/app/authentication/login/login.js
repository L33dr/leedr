'use strict';

angular.module('myApp.login', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/login', {
    templateUrl: 'authentication/login/login.html',
    controller: 'LoginCtrl'
  });
}])

.controller('LoginCtrl', ['$scope', '$rootScope', 'AUTH_EVENTS', 'AuthService', '$location', function($scope, $rootScope, AUTH_EVENTS, AuthService, $location) {
        // Initializes the credential fields
        $scope.credentials = {
            username: '',
            password: ''
        };

        $scope.submit = function (credentials) {

            // Calls the login function, passing the credentials.
            // On success it will broadcast the login success event
            // set the current user then redirect to home page.
          AuthService.login(credentials).then(function (user) {
              $rootScope.$broadcast(AUTH_EVENTS.loginSuccess);
              $scope.setCurrentUser(user);
              $location.path('/');
              toastr.success("You logged in successfully.")
          }, function() {
              $rootScope.$broadcast(AUTH_EVENTS.loginFailed);
              toastr.error("Please try again.")
          });
        };
}]);