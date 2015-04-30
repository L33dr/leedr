'use strict';

// Declare app level module which depends on views, and components
angular.module('myApp', [
    'ngRoute',
    'ngCookies',
    'LocalStorageModule',
    'myApp.main',
    'myApp.register',
    'myApp.view1',
    'myApp.login',
    'myApp.logout',
    'myApp.confirmEmail',
    'restangular'
]).
    config(['$routeProvider', 'RestangularProvider', '$httpProvider', function ($routeProvider, RestangularProvider, $httpProvider) {
        $routeProvider.otherwise({redirectTo: '/view1'});
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

    service('Session', function () {
        this.create = function (username) {
            this.username = username;
        };

        this.destroy = function () {
            this.username = null;
        }
    }).

    factory('AuthService', ['$http', 'Session', 'Restangular', 'localStorageService', function

        /*
         This is the base authentication service. This will reach out to the backend and do the authentication.
         This is where the MainCtrl looks to see if a user is authenticated. Services come here to run the login and logout functions.
         */
        ($http, Session, Restangular, localStorageService) {
        var authService = {};

        authService.login = function (credentials) {
            return Restangular.one('rest-auth/login').customPOST(credentials).then(function (key) {
                // Sets the default header so the backend knows which user is authenticated.
                Restangular.configuration.defaultHeaders.authorization = 'Token ' + key.key;
                return Restangular.all('rest-auth/user').customGET().then(function (res) {
                    // Save key to local storage once it works.
                    localStorageService.add('token', key.key);
                    // Create session.
                    Session.create(res.username);
                    return res;
                });

            });
        };

        authService.logout = function () {
            return Restangular.one('rest-auth/logout').customPOST().then(function () {
                // Removes local storage key for token and destroys the token.
                Restangular.configuration.defaultHeaders.authorization = '';
                localStorageService.remove('token');
                Session.destroy();
                return true
            }, function (error) {
                // Removes it anyways as we will have them reloggin.
                Restangular.configuration.defaultHeaders.authorization = '';
                localStorageService.remove('token');
                Session.destroy();
                return error
            });
        };

        authService.isAuthenticated = function () {
            // Doesn't do a whole lot yet.
            return !!Session.username;
        };


        return authService;
    }
    ]).
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
    })
;

    $("#menu-toggle").click(function (e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });

