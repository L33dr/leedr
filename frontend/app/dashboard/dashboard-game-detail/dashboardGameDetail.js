'use strict';

angular.module('myApp.dashboardGameDetail', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/dashboard/game-detail/:gameShorthand', {
            templateUrl: 'dashboard/dashboard-game-detail/dashboard-game-detail.html',
            controller: 'DashboardGameDetailCtrl'
        });
    }])

    .controller('DashboardGameDetailCtrl', ['$scope', '$routeParams', '$location', '$timeout', 'Restangular', 'gameService',
        function ($scope, $routeParams, $location, $timeout, Restangular, gameService) {

            $scope.templateUrl = 'dashboard/dashboard-game-views/' + $routeParams.gameShorthand + '.html';

            // Checks to see if the game in the route params is a game we support and that a user is logged in.
            // If so, it will get the url from the
            //      gameService and pull in the data and assign it to the scope.
            $timeout(function () {
            if (gameService[$routeParams.gameShorthand] && $scope.user) {

                    Restangular.all(gameService[$routeParams.gameShorthand].url).customGET().then(function (data) {
                        if (data[0]) {
                            $scope.GameData = data[0];

                        } else {
                            $location.path("/dashboard");
                            toastr.error("We are still updating your data. Please check back later.");
                        }
                    }, function (error) {
                        toastr.error("Something went wrong retrieving your data. Here is the error message: " + error);
                        $location.path("/dashboard");
                    })
            } else if ($scope.user && !gameService[$routeParams.gameShorthand]) {
                // If the game is not in our supported list it will redirect them to the home page.
                toastr.error("Could not find that game!");
                $location.path('/dashboard');
            }
            }, 250)
        }]);