'use strict';

angular.module('myApp.test', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/test', {
            templateUrl: 'test/test.html',
            controller: 'TestCtrl'
        });
    }])

    .controller('TestCtrl', ['$scope', '$timeout', 'Session', 'Restangular', function ($scope, $timeout, Session, Restangular) {
        $scope.currentSession = Session.get();
        if ($scope.currentSession.username !== null) {
            $timeout(function () {
                Restangular.one('/leedr/user-game-profile').customGET().then(function (data) {
                    $scope.profile = data;
                });
            }, 100);
        }
    }]);