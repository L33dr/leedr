'use strict';

angular.module('myApp.dashboardHome', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/dashboard', {
            templateUrl: 'dashboard/dashboard-home/dashboard-home.html',
            controller: 'DashboardHomeCtrl'
        });
    }])

    .controller('DashboardHomeCtrl', ['$scope', '$location', '$timeout', 'Restangular', 'Session', function ($scope, $location, $timeout, Restangular, Session) {
        $scope.isLoggedIn = false;

        // User is required to be logged in before they can view this page.
        $timeout(function () {
            $scope.isLoggedIn = Session.requireLogin();
        }, 100).then(function () {
            if ($scope.isLoggedIn) {
                if (!$scope.user.username) {
                    Restangular.all('/leedr/user-profile').customGET().then(function (data) {
                        $scope.user = data[0];
                    });
                }
            }
        });


    }]);