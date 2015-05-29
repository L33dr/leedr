'use strict';

angular.module('myApp.dashboardAddGame', ['ngRoute'])
    .controller('DashboardAddGameCtrl', ['$scope', '$timeout', '$location', '$modalInstance', 'Restangular', 'gameService', 'AuthService',
        function ($scope, $timeout, $location, $modalInstance, Restangular, gameService, AuthService) {
            $scope.games = gameService;
            $scope.allGames = gameService;
            $scope.showRealm = false;

            $scope.toggleSc2Help = function () {
                $scope.sc2Help = !$scope.sc2Help
            };


            $scope.submit = function () {
                $scope.usergame.game.shorthand_name = Object.keys(gameService).filter(function (key) {
                    return gameService[key] === $scope.usergame.game
                })[0];

                Restangular.all("leedr/user-game-profile").customPOST($scope.usergame).then(function (data) {
                    $timeout(function () {
                        AuthService.updateUserInfo();
                        toastr.success("We have added your game. It may take a bit for stats to arrive!");
                        $modalInstance.close();
                        $location.path('/dashboard');
                    }, 500);
                }, function (error) {
                    toastr.error("Something went wrong retrieving your data. Here is the error message: " + '"' + error.data + '"');
                })
            };

            $scope.cancel = function () {
                $modalInstance.dismiss('cancel');
            };

            // Needing to convert the games object to an array so we can use a select box on it.
            $scope.games = [];
            for (var i in gameService) {
                if (gameService.hasOwnProperty(i)) {
                    $scope.games.push(gameService[i]);
                }
            }

        }]);