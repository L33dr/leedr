'use strict';

angular.module('myApp.dashboardGameDetail', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/dashboard/game-detail/:gameShorthand',  {
            templateUrl: 'dashboard/dashboard-game-detail/dashboard-game-detail.html',
            controller: 'DashboardGameDetailCtrl'
        });
    }])

    .controller('DashboardGameDetailCtrl', ['$scope', '$routeParams', 'Restangular', function ($scope, $routeParams, Restangular) {
        $scope.templateUrl = 'dashboard/dashboard-game-views/' + $routeParams.gameShorthand + '.html';
        if ($routeParams.gameShorthand == "LOL") {
            Restangular.all('leedr/LOL/user-data/').customGET().then( function(data){
                $scope.LOLData = data;
            });
        }
    }]);