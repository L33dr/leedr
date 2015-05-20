'use strict';
/*
 This is the main controller for the front end application. use this controller to make changes to navbar/home page.
 Active user will be set on this scope as it will be the highest on the DOM.
 */

angular.module('myApp.main', ['ngRoute']).controller('ApplicationCtrl', ['$scope', '$rootScope', 'AuthService', 'Restangular', 'Session', 'localStorageService',
    function ($scope, $rootScope, AuthService, Restangular, Session, localStorageService) {

        // Initializes variables used throughout whole application.

        $scope.currentUser = null;
        $scope.smWrapper = false;

        // This will load the current user if they are still signed in.
        var token = localStorageService.get('token');

        if (token) {
            // Add token to default headers.
            Restangular.configuration.defaultHeaders.authorization = 'Token ' + token;
            $rootScope.loginInProcess = true;
            // Get the user profile data using the existing token from previous login
            Restangular.all('leedr/user-profile').customGET().then(function (res) {
                $rootScope.loginInProcess = false;
                var user_data = res[0];
                Session.create(user_data.user.username, user_data.user.first_name, user_data.user.last_name,
                    user_data.user.email, user_data.premium, user_data.games);
                Session.get();

            }, function (error) {
                $rootScope.loginInProcess = false;
                // ERROR with token. Remove it from local storage.
                localStorageService.remove('token');

            });
        }

        $rootScope.$on('$locationChangeSuccess', function(event) {
            $scope.closePopOuts();
        });

        $scope.closePopOuts = function () {
            $scope.showSignup = false;
            $scope.showLogin = false;
            $scope.showLogout = false;
            $scope.popoutNavOpen = false;
            $("#main-body").removeClass("toggledPopOut");
        };

        $scope.toggleEntireNav = function () {
            if ($scope.showSignup || $scope.showLogin || $scope.showLogout) {
                $scope.closePopOuts();
                setTimeout(function () {
                    $("#wrapper-sm").toggleClass("toggled");
                    $("#wrapper").toggleClass("toggled");
                    $("#main-body").toggleClass("toggled");

                }, 275);
            } else {
                setTimeout(function () {
                    $("#wrapper-sm").toggleClass("toggled");
                    $("#wrapper").toggleClass("toggled");
                    $("#main-body").toggleClass("toggled");
                }, 275);
            }
        };

        $scope.showSignup = false;

        $scope.toggleSignup = function () {
            if (!$scope.showSignup) {
                $scope.closePopOuts();
                $scope.popoutNavOpen = true;
                $("#main-body").addClass("toggledPopOut");
                $scope.showSignup = !$scope.showSignup;
            } else {
                $scope.closePopOuts();
            }
        };

        $scope.showLogin = false;

        $rootScope.toggleLogin = function (force) {
            if (!$scope.showLogin) {
                $scope.closePopOuts();
                $scope.popoutNavOpen = true;
                $("#main-body").addClass("toggledPopOut");
                if (force) {
                    $scope.showLogin = true;
                } else {
                    $scope.showLogin = !$scope.showLogin;
                }
            } else {
                $scope.closePopOuts();
            }
        };

        $scope.showLogout = false;

        $scope.toggleLogout = function () {
            if (!$scope.showLogout) {
                $scope.closePopOuts();
                $scope.popoutNavOpen = true;
                $("#main-body").addClass("toggledPopOut");
                $scope.showLogout = !$scope.showLogout;
            } else {
                $scope.closePopOuts();
            }
        };

    }]);

