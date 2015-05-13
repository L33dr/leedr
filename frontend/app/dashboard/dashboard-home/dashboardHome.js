'use strict';

angular.module('myApp.dashboardHome', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/dashboard', {
            templateUrl: 'dashboard/dashboard-home/dashboard-home.html',
            controller: 'DashboardHomeCtrl'
        });
    }])

    .controller('DashboardHomeCtrl', ['$scope', 'Restangular', function ($scope, Restangular) {
        Restangular.all('/leedr/user-profile').customGET().then(function(data) {
            $scope.userprofile = data[0];
        });
    }]);