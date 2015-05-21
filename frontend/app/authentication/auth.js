angular.module('myApp.auth', ['ngRoute']).
    service('Session', ['$rootScope', function ($rootScope) {
        this.create = function (username, first_name, last_name, email, premium, games) {
            this.username = username;
            this.first_name = first_name;
            this.last_name = last_name;
            this.email = email;
            this.premium = premium;
            this.games = games;
        };

        this.destroy = function () {
            this.username = null;
            this.first_name = null;
            this.last_name = null;
            this.email = null;
            this.premium = null;
            this.games = null;
        };

        this.get = function () {
            $rootScope.user = {
                'username': this.username,
                'first_name': this.first_name,
                'last_name': this.last_name,
                'email': this.email,
                'premium': this.premium,
                'games': this.games
            };
            return $rootScope.user
        };

    }
    ]).
    factory('AuthService', ['$http', 'Session', 'Restangular', 'localStorageService', function
        ($http, Session, Restangular, localStorageService) {

        /*
         This is the base authentication service. This will reach out to the backend and do the authentication.
         This is where the MainCtrl looks to see if a user is authenticated. Services come here to run the login and logout functions.
         */
        var authService = {};

        authService.login = function (credentials) {
            return Restangular.one('rest-auth/login').customPOST(credentials).then(function (key) {
                // Sets the default header so the backend knows which user is authenticated.
                Restangular.configuration.defaultHeaders.authorization = 'Token ' + key.key;
                return Restangular.all('leedr/user-profile').customGET().then(function (res) {
                    // Save key to local storage once it works.
                    localStorageService.add('token', key.key);
                    // Create session.
                    var user_data = res[0];
                    Session.create(user_data.user.username, user_data.user.first_name, user_data.user.last_name,
                        user_data.user.email, user_data.premium, user_data.games);
                    Session.get();
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
                Session.get();
                return true
            }, function (error) {
                // Removes it anyways as we will have them reloggin.
                Restangular.configuration.defaultHeaders.authorization = '';
                localStorageService.remove('token');
                Session.destroy();
                Session.get();
                return error
            });
        };

        authService.isAuthenticated = Session.username !== null && typeof Session.username !== 'undefined';
        return authService;
    }])
    .service('RequireLogin', ['$rootScope', '$location', '$timeout', 'Restangular', 'localStorageService', 'Session', function ($rootScope, $location, $timeout, Restangular, localStorageService, Session) {

        var redirect = function (path) {
            // This will redirect the user to the home page and open up the login popout.
            $location.path("/");
            $timeout(function () {
                $rootScope.toggleLogin(true, path);
                toastr.error("You must be logged in to view this page.");
            }, 100);
        };

        $rootScope.$on('$routeChangeStart', function (event, next, current) {
            // The regex below matches anything that starts with /dashboard
            if ((/\/dashboard([A-Za-z0-9-/:]*)/.test(next.$$route.originalPath)) && !$rootScope.user) {
                // Stopping the route from continuing
                event.preventDefault();
                var path = '';
                if (next.$$route.keys[0]) {
                    path = next.$$route.originalPath;
                    path = path.slice(1, path.indexOf(':')) + next.params[next.$$route.keys[0]['name']];
                } else {
                    path = next.$$route.originalPath.slice(1, next.$$route.originalPath.length) + '/';
                }

                // Seeing if user is still 'logged in' by grabbing the token.
                // If they are logged in we will grab their profile information and setup the session.
                // Finally we redirect them back to their original path, if possible.
                var token = localStorageService.get('token');
                if (token) {
                    Restangular.configuration.defaultHeaders.authorization = 'Token ' + token;
                    Restangular.all('leedr/user-profile').customGET().then(function (res) {
                        var user_data = res[0];
                        Session.create(user_data.user.username, user_data.user.first_name, user_data.user.last_name,
                            user_data.user.email, user_data.premium, user_data.games);
                        Session.get();
                        $location.path(path);
                        // If their token is invalid we simply redirect them to the login.
                        // Once they complete the login they will then be redirected back to original requested page.
                    }, function (error) {
                        localStorageService.remove('token');
                        redirect(path);
                    });
                    // If they are not logged in, we simply redirect them to the login.
                    // Once they complete the login they will then be redirected back to original requested page.
                } else {
                    event.preventDefault();
                    redirect(path);
                }
            }
        });

    }]);