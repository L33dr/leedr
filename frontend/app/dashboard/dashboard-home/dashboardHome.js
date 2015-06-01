'use strict';

angular.module('myApp.dashboardHome', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/dashboard', {
            templateUrl: 'dashboard/dashboard-home/dashboard-home.html',
            controller: 'DashboardHomeCtrl'
        });
    }])

    .controller('DashboardHomeCtrl', ['$scope', '$location', '$timeout', '$modal', '$interval', 'Restangular', 'Session',
        'gameService', 'AuthService', function ($scope, $location, $timeout, $modal, $interval, Restangular, Session, gameService, AuthService) {

            $scope.supportedGames = gameService;


            $scope.openSettings = function () {
                $scope.closePopOuts();
                var modalInstance = $modal.open({
                    templateUrl: 'dashboard/dashboard-user-profile/dashboard-user-profile.html',
                    controller: 'DashboardUserProfileCtrl',
                    size: 'lg'
                });
            };

            $scope.openGameModal = function () {
                $scope.closePopOuts();
                var modalInstance = $modal.open({
                    templateUrl: 'dashboard/dashboard-add-game/dashboard-add-game.html',
                    controller: 'DashboardAddGameCtrl',
                    size: 'lg'
                });

                modalInstance.result.then(function () {
                    $scope.hasGames = $scope.user.games != 0;
                });

            };
            try {
                $scope.hasGames = $scope.user.games != 0;
            } catch (ex) {
                // If the user has no games it will show undefined and throw an error.
            }

            var updateProfile = function () {
                var user = $scope.user;
                AuthService.updateUserInfo().then(function () {
                    if (user !== $scope.user) {
                        $scope.hasGames = $scope.user.games != 0;
                    }
                });
            };

            updateProfile();

            var stop = $interval(function () {
                updateProfile();
            }, 60000);


            $scope.$on('$destroy', function () {
                $interval.cancel(stop);
            });
        }]);