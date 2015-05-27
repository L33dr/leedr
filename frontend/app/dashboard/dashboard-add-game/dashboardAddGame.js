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
              console.log($scope.usergame);
                $scope.usergame.game.shorthand_name = Object.keys(gameService).filter(function(key) {return gameService[key] === $scope.usergame.game})[0];

              Restangular.all("leedr/user-game-profile").customPOST($scope.usergame).then(function (data) {
                    console.log(data);
                    }, function (error) {
                        toastr.error("Something went wrong retrieving your data. Here is the error message: " + error);
                        $location.path("/dashboard");
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