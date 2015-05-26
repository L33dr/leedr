angular.module('myApp.gameService', ['ngRoute']).
    service('gameService', function () {
        var games = {
            "LOL": {
                "name": "League Of Legends",
                "url": "leedr/LOL/user-data/",
                "thumbnail": "https://signup.leagueoflegends.com/theme/signup_theme/img/signup_logo2.png"
            },
            "SC2": {
                "name": "Star Craft 2",
                "url": "leedr/SC2/user-data/",
                "thumbnail": "https://upload.wikimedia.org/wikipedia/de/f/f1/Starcraft2_logo.png"
            }
        };
        return games
    });