'use strict';

angular.module('myApp.dashboardGameDetail', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/dashboard/game-detail/:gameShorthand', {
            templateUrl: 'dashboard/dashboard-game-detail/dashboard-game-detail.html',
            controller: 'DashboardGameDetailCtrl'
        });
    }])

    .controller('DashboardGameDetailCtrl', ['$scope', '$routeParams', '$location', 'Restangular', 'gameService',
        function ($scope, $routeParams, $location, Restangular, gameService) {

            // Will set the base template to use for this game we are loading.
            $scope.templateUrl = 'dashboard/dashboard-game-views/' + $routeParams.gameShorthand + '.html';

            // Checks to see if the game in the route params is a game we support. If so, it will get the url from the
            //      gameService and pull in the data and assign it to the scope.
            if (gameService[$routeParams.gameShorthand]) {
                Restangular.all(gameService[$routeParams.gameShorthand].url).customGET().then(function (data) {
                    $scope.GameData = data;
                }, function(error) {
                    toastr.error("Something went wrong retrieving your data. Here is the error message: " + error);
                    $location.path("/dashboard");
                });
            }else {
                // If the game is not in our supported list it will redirect them to the home page.
                toastr.error("Could not find that game! Redirecting you to the home page. :(");
                $location.path('/');

            }
        }]);