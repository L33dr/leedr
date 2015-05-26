'use strict';

// Declare app level module which depends on views, and components
angular.module('myApp', [
    'ngRoute',
    'ngCookies',
    'ngAnimate',
    'LocalStorageModule',
    'myApp.main',
    'myApp.auth',
    'myApp.home',
    'myApp.register',
    'myApp.test',
    'myApp.gameService',
    'myApp.dashboardHome',
    'myApp.dashboardGameDetail',
    'myApp.dashboardUserProfile',
    'myApp.dashboardAddGame',
    'myApp.view1',
    'myApp.login',
    'myApp.logout',
    'myApp.confirmEmail',
    'restangular',
    'ui.bootstrap'
]).
    config(['$routeProvider', 'RestangularProvider', '$httpProvider', function ($routeProvider, RestangularProvider, $httpProvider) {
        $routeProvider.otherwise({redirectTo: '/home'});
        RestangularProvider.setBaseUrl('http://localhost:8001');
        RestangularProvider.setRequestSuffix('/');
        $httpProvider.interceptors.push([
            '$injector',
            function ($injector) {
                return $injector.get('AuthInterceptor');
            }
        ]);
    }]).
    // TODO:  Do something on these events. Probably redirect.
    constant('AUTH_EVENTS', {
        loginSuccess: 'auth-login-success',
        loginFailed: 'auth-login-failed',
        logoutSuccess: 'auth-logout-success',
        sessionTimeout: 'auth-session-timeout',
        notAuthenticated: 'auth-not-authenticated',
        notAuthorized: 'auth-not-authorized'
    }).
    factory('AuthInterceptor', function ($rootScope, $q,
                                         AUTH_EVENTS) {
        return {
            responseError: function (response) {
                $rootScope.$broadcast({
                    401: AUTH_EVENTS.notAuthenticated,
                    403: AUTH_EVENTS.notAuthorized,
                    419: AUTH_EVENTS.sessionTimeout,
                    440: AUTH_EVENTS.sessionTimeout
                }[response.status], response);
                return $q.reject(response);
            }
        };
    });

