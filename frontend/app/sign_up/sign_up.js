'use strict';

angular.module('myApp.sign_up', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/sign_up', {
    templateUrl: 'sign_up/sign_up.html',
    controller: 'SignupCtrl'
  });
}])

.controller('SignupCtrl', [function() {
       $("a.first").pageslide({
       direction: "right", // left or right
       modal: false, // If modal is set to ‘true’, then you must explicitly close PageSlide using $.pageslide.close()
       speed: 'normal', // The speed at which the page slides over.
       iframe: true // Linked pages are loaded into an iframe
    });
}]);