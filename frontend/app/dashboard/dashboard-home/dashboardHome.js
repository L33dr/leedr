'use strict';

angular.module('myApp.dashboardHome', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/dashboard', {
            templateUrl: 'dashboard/dashboard-home/dashboard-home.html',
            controller: 'DashboardHomeCtrl'
        });
    }])

    .controller('DashboardHomeCtrl', ['$scope', '$location', 'Restangular', 'Session', function ($scope, $location, Restangular, Session) {
        if (Session.requireLogin()) {
            Restangular.all('/leedr/user-profile').customGET().then(function (data) {
                $scope.userprofile = data[0];
            });
        }
    }]);