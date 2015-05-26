'use strict';

angular.module('myApp.dashboardUserProfile', ['ngRoute'])
    .controller('DashboardUserProfileCtrl', ['$scope', '$modalInstance', 'Restangular',
        function ($scope, $modalInstance, Restangular) {
            $scope.userUpdate = angular.copy($scope.user);

            $scope.submit = function () {
                if ($scope.userUpdate.password1 && $scope.userUpdate.password2 && $scope.userUpdate.password1 == $scope.userUpdate.password2) {
                    var data = {
                        new_password1: $scope.userUpdate.password1,
                        new_password2: $scope.userUpdate.password2
                    };
                    Restangular.one('/rest-auth/password/change/')
                        .customPOST(data).then(function () {
                            toastr.success("Password updated!");
                        }, function (error) {
                            console.log(error);
                            toastr.error('Password change error! Please double check fields.');
                        }
                    )
                }
                delete $scope.userUpdate.password1;
                delete $scope.userUpdate.password2;
                if ($scope.userUpdate !== $scope.user) {
                    var user = {
                        user: {
                            username: $scope.userUpdate.username,
                            first_name: $scope.userUpdate.first_name,
                            last_name: $scope.userUpdate.last_name
                        },
                        games: $scope.user.games
                    };
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