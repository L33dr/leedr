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
            $scope.templateUrl = 'dashboard/dashboard-game-views/' + $routeParams.gameShorthand + '.html';
            if (gameService[$routeParams.gameShorthand]) {
                Restangular.all(gameService[$routeParams.gameShorthand].url).customGET().then(function (data) {
                    $scope.GameData = data;
                });
            }else {
                toastr.error("Could not find that game! Redirecting you to the home page. :(");
                $location.path('/');

            }


        }]);


//# Games service
//# Filter based on service
//# get urls out of controller