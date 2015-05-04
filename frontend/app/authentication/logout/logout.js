'use strict';

angular.module('myApp.logout', ['ngRoute'])

.controller('LogoutCtrl', ['$scope', 'AuthService', '$location', function($scope, AuthService, $location) {
        // Calls the logout function of the authservice, removes current user and redirects to home page.
    $scope.submit = function() {
        AuthService.logout();
        $scope.setCurrentUser(null);
        $location.path('/');
        toastr.success("You logged out successfully.");
        $scope.closePopOuts();
    };
}]);