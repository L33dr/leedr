'use strict';

angular.module('myApp.logout', ['ngRoute'])

    .controller('LogoutCtrl', ['$scope', 'AuthService', '$location', 'Session',
        function ($scope, AuthService, $location, Session) {
            // Calls the logout function of the authservice, removes current user and redirects to home page.
            $scope.submit = function () {
                AuthService.logout();
                $location.path('/');
                toastr.success("You logged out successfully.");
                $scope.closePopOuts();
            };
        }]);