'use strict';

angular.module('myApp.logout', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/logout', {
    templateUrl: 'authentication/logout/logout.html',
    controller: 'LogoutCtrl'
  });
}])

.controller('LogoutCtrl', ['$scope', 'AuthService', '$location', function($scope, AuthService, $location) {
        // Calls the logout function of the authservice, removes current user and redirects to home page.
    $scope.submit = function() {
        AuthService.logout();
        $scope.setCurrentUser(null);
        $location.path('/');
    };
}]);