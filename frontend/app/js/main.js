'use strict';
/*
This is the main controller for the front end application. use this controller to make changes to navbar/home page.
Active user will be set on this scope as it will be the highest on the DOM.
 */

angular.module('myApp.main', ['ngRoute']).controller('ApplicationCtrl', ['$scope', 'AuthService', 'Restangular', 'Session', 'localStorageService',
    function ($scope, AuthService, Restangular, Session, localStorageService) {

        // Initializes variables used throughout whole application.

        $scope.currentUser = null;
        $scope.setCurrentUser = function (user) {
            $scope.currentUser = user;
        };

        // This will load the current user if they are still signed in.
        var token = localStorageService.get('token');

        if (token) {
            // Add token to default headers.
            Restangular.configuration.defaultHeaders.authorization = 'Token ' + token;
            Restangular.all('rest-auth/user').customGET().then(function (res) {
                Session.create(res.username);
                $scope.setCurrentUser(res);
                $scope.isAuthorized = AuthService.isAuthenticated();

            }, function (error) {
                // ERROR with token. Remove it from local storage.
                localStorageService.remove('token');

            });
        }

        $scope.closePopOuts = function() {
            $scope.showSignup = false;
            $scope.showLogin = false;
            $scope.showLogout = false;
            $("#main-body").removeClass("toggledPopOut");
            $("#menu-toggle").removeClass("toggledPopOut");
        };

        $scope.toggleEntireNav = function() {
            if ($scope.showSignup || $scope.showLogin || $scope.showLogout) {
                $scope.closePopOuts();
                setTimeout(function () {
                    $("#wrapper").toggleClass("toggled");
                    $("#main-body").toggleClass("toggled");
                    $("#menu-toggle").toggleClass("toggled");
                }, 500);
            } else {
                $("#wrapper").toggleClass("toggled");
                $("#main-body").toggleClass("toggled");
                $("#menu-toggle").toggleClass("toggled");
            }
        };

        $scope.showSignup = false;

        $scope.toggleSignup = function () {
            if (!$scope.showSignup) {
                $scope.closePopOuts();
                $("#main-body").addClass("toggledPopOut");
                $("#menu-toggle").addClass("toggledPopOut");
                $scope.showSignup = !$scope.showSignup;
            } else {
                $scope.closePopOuts();
            }
        };

        $scope.showLogin = false;

        $scope.toggleLogin = function () {
            if (!$scope.showLogin) {
                $scope.closePopOuts();
                $("#main-body").addClass("toggledPopOut");
                $("#menu-toggle").addClass("toggledPopOut");
                $scope.showLogin = !$scope.showLogin;
            } else {
                $scope.closePopOuts();
            }
        };

        $scope.showLogout = false;

        $scope.toggleLogout = function () {
            if (!$scope.showLogout) {
                $scope.closePopOuts();
                $("#main-body").addClass("toggledPopOut");
                $("#menu-toggle").addClass("toggledPopOut");
                $scope.showLogout = !$scope.showLogout;
            } else {
                $scope.closePopOuts();
            }
        };

    }]);

