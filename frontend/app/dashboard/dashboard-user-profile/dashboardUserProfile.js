'use strict';

angular.module('myApp.dashboardUserProfile', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/dashboard/user-profile/', {
            templateUrl: 'dashboard/dashboard-user-profile/dashboard-user-profile.html',
            controller: 'DashboardUserProfileCtrl'
        });
    }])

    .controller('DashboardUserProfileCtrl', ['$scope', '$modalInstance', 'Restangular',
        function ($scope, $modalInstance, Restangular) {
            $scope.userUpdate = angular.copy($scope.user);

            var getChanges = function (prev, now) {
                var changes = {};
                var prop = {};
                var c = {};

                for (prop in now) { //ignore jslint
                    if (prop.indexOf("_KO") > -1) {
                        continue; //ignore jslint
                    }

                    if (!prev || prev[prop] !== now[prop]) {
                        if (_.isArray(now[prop])) {
                            changes[prop] = now[prop];
                        }
                        else if (_.isObject(now[prop])) {
                            // Recursion alert
                            c = um.utils.getChanges(prev[prop], now[prop]);
                            if (!_.isEmpty(c)) {
                                changes[prop] = c;
                            }
                        } else {
                            changes[prop] = now[prop];
                        }
                    }
                }

                return changes;
            };

            $scope.submit = function () {
                if ($scope.userUpdate !== $scope.user) {
                    var user = {
                        user: {
                            username: $scope.userUpdate.username,
                            first_name: $scope.userUpdate.first_name,
                            last_name: $scope.userUpdate.last_name
                        },
                        games: $scope.user.games
                    };
                    console.log(user.games);
                    Restangular.one('/leedr/user-profile/update').patch(user).then(function () {
                        $modalInstance.close('submitted!');
                        toastr.success("Profile updated!");
                    }, function () {
                        toastr.error("Profile update failed! Please double check everything!");
                    });
                }
            };

            $scope.cancel = function () {
                $modalInstance.dismiss('cancel');
            };
        }]);