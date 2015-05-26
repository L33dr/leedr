'use strict';

angular.module('myApp.dashboardAddGame', ['ngRoute'])
        .controller('DashboardAddGameCtrl', ['$scope', '$modalInstance', 'Restangular', 'gameService',
        function ($scope, $modalInstance, Restangular, gameService) {
            $scope.games = gameService;
            $scope.allGames = gameService;
            $scope.showRealm = false;

            $scope.toggleSc2Help = function() {
                $scope.sc2Help = !$scope.sc2Help
            };


            $scope.submit = function () {
              toastr.error("Not implemented yet!");
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