'use strict';
/*
 This is the main controller for the front end application. use this controller to make changes to navbar/home page.
 Active user will be set on this scope as it will be the highest on the DOM.
 */

angular.module('myApp.main', ['ngRoute']).controller('ApplicationCtrl', ['$scope', '$rootScope', 'RequireLogin', function ($scope, $rootScope, RequireLogin) {

        // Initializes variables used throughout whole application.
        $scope.currentUser = null;
        $scope.smWrapper = false;

        $rootScope.$on('$routeChangeStart', function (event) {
            $scope.closePopOuts();
        });

        $scope.closePopOuts = function () {
            $scope.showSignup = false;
            $scope.showLogin = false;
            $scope.showLogout = false;
            $scope.popoutNavOpen = false;
            if ($("#login").hasClass("show")) {
                $("#login").removeClass("show");
            }
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
                $scope.showSignup = true;
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
                $scope.showLogin = true;
                if (force) {
                    $("#login").addClass("show");
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
                $scope.showLogout = true;
            } else {
                $scope.closePopOuts();
            }
        };

    }]);

