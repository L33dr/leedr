angular.module('myApp.gameService', ['ngRoute']).
    service('gameService', function () {
        var games = {
            "LOL": {
                "name": "League Of Legends",
                "url": "leedr/LOL/user-data/"
            },
            "SC2": {
                "name": "Star Craft 2",
                "url": "leedr/SC2/user-data/"
            }
        };
        return games
    });