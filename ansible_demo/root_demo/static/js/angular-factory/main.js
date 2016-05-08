var app = angular.module('myApp', ['ngResource','ipCookie', 'angularUtils.directives.dirPagination', 'ui.bootstrap','ui.router','ui.ace','angular-md5','base64']);
    app.config(function($interpolateProvider) { 
      $interpolateProvider.startSymbol('((');
      $interpolateProvider.endSymbol('))');
    });
    app.run(
    function($http) {
        //$http.defaults.headers.post['X-CSRFToken'] = $.cookie('csrftoken');
        // Add the following two lines
        $http.defaults.xsrfCookieName = 'csrftoken';
        $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    });


