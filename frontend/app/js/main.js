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

            // Get the user profile data using the existing token from previous login
            Restangular.all('leedr/user-profile').customGET().then(function (res) {
                var user_data = res[0];
                Session.create(user_data.user.username, user_data.user.first_name, user_data.user.last_name,
                        user_data.user.email, user_data.premium, user_data.games);
                Session.get();

            }, function (error) {
                // ERROR with token. Remove it from local storage.
                localStorageService.remove('token');

            });
        }

        $scope.closePopOuts = function () {
            $scope.showSignup = false;
            $scope.showLogin = false;
            $scope.showLogout = false;
            $("#menu-toggle-in-nav").removeClass("hidden");
            $("#main-body").removeClass("toggledPopOut");
        };

        $scope.toggleEntireNav = function () {
            if ($scope.showSignup || $scope.showLogin || $scope.showLogout) {
                $scope.closePopOuts();
                var smallNavOpen = $("#wrapper-sm").hasClass("toggled");
                setTimeout(function () {
                    if (!smallNavOpen) {
                        $("#wrapper-sm").toggleClass("toggled");
                    } else {
                        setTimeout(function () {
                            $("#wrapper-sm").toggleClass("toggled");
                        }, 250);
                    }
                    $("#wrapper").toggleClass("toggled");
                    $("#main-body").toggleClass("toggled");

                }, 500);
            } else {
                setTimeout(function () {
                    if (!smallNavOpen) {
                        $("#wrapper-sm").toggleClass("toggled");
                    } else {
                        setTimeout(function () {
                            $("#wrapper-sm").toggleClass("toggled");
                        }, 250);
                    }
                    $("#wrapper").toggleClass("toggled");
                    $("#main-body").toggleClass("toggled");

                }, 500);
            }
        };

        $scope.showSignup = false;

        $scope.toggleSignup = function () {
            if (!$scope.showSignup) {
                $scope.closePopOuts();
                $("#main-body").addClass("toggledPopOut");
                $("#menu-toggle-in-nav").addClass("hidden");
                $scope.showSignup = !$scope.showSignup;
            } else {
                $scope.closePopOuts();
            }
        };

        $scope.showLogin = false;

        $rootScope.forceShowLogin = function() {
            $scope.closePopOuts();
            $scope.showLogin = true;
        };

        $scope.toggleLogin = function () {
            if (!$scope.showLogin) {
                $scope.closePopOuts();
                $("#main-body").addClass("toggledPopOut");
                $("#menu-toggle-in-nav").addClass("hidden");
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
                $("#menu-toggle-in-nav").addClass("hidden");
                $scope.showLogout = !$scope.showLogout;
            } else {
                $scope.closePopOuts();
            }
        };

    }]);

