'use strict';

angular.module('myApp.dashboardHome', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/dashboard', {
            templateUrl: 'dashboard/dashboard-home/dashboard-home.html',
            controller: 'DashboardHomeCtrl'
        });
    }])

    .controller('DashboardHomeCtrl', ['$scope', '$location', '$timeout', '$modal', 'Restangular', 'Session', function ($scope, $location, $timeout, $modal, Restangular, Session) {
        $scope.isLoggedIn = false;

        // User is required to be logged in before they can view this page.
        $timeout(function () {
            $scope.isLoggedIn = Session.requireLogin();
        }, 100).then(function () {
            if ($scope.isLoggedIn) {
                if (!$scope.user.username) {
                    // The likeliness of this being called is very slim.
                    // However, in the case that the user is not logged in or does not have the data on the scope it will call it here.
                    Restangular.all('/leedr/user-profile').customGET().then(function (data) {
                        $scope.user = data[0];
                    });
                }
            }
        });

        $scope.openSettings = function() {
            $scope.closePopOuts();
            var modalInstance = $modal.open({
                templateUrl: 'dashboard/dashboard-user-profile/dashboard-user-profile.html',
                controller: 'DashboardUserProfileCtrl',
                size: 'lg'
            });

        }


    }]);