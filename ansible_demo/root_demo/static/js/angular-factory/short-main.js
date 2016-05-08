var routeapp = angular.module('RouteApp', ['angularUtils.directives.dirPagination', 'ngResource','ui.select2','ipCookie','ui.bootstrap','ui.router','ui.ace','angular-md5','base64','ngFileUpload']);
    routeapp.config(function($interpolateProvider) { 
      $interpolateProvider.startSymbol('((');
      $interpolateProvider.endSymbol('))');
    })
    routeapp.config(function($stateProvider, $locationProvider){
    $stateProvider
        .state('welcome_page', {                //备份代码
            templateUrl: "/release/welcome_page/",
            params: {new_param: null}
        })
        .state('search_branch', {
            templateUrl: "/release/search_branch/",
            params: {new_param: null}
        })
        .state('publish', {
            templateUrl: "/release/publish/",
            controller : 'pull_code_ctrl',
            params: {new_param: null}
        })
        .state('increase', {
            templateUrl: "/release/increase/",
            params: {new_param: null}
        })  
        .state('servers_config', {
            templateUrl: "/release/servers_config/",
            params: {new_param: null}
        })
        .state('release_code_request', {
            templateUrl: "/release/release_code_request/",
            params: {new_param: null}
        })
        .state('enlarge_request', {
            templateUrl: "/release/increase_request/",
            params: {new_param: null}
        })  
        .state('database_update', {
            templateUrl: "/release/database_update/",
            params: {new_param: null}
        })
        .state('process_reset', {
            templateUrl: "/release/process_reset/",
            params: {new_param: null}
        })
        .state('costume_operation', {
            templateUrl: "/release/costume_operation/",
            params: {new_param: null}
        })
        .state('log_view', {
            templateUrl: "/release/log_view/",
            params: {new_param: null}
        })
        .state('global_settings', {
            templateUrl: "/release/global_settings/",
            params: {new_param: null}
        })
         $locationProvider.html5Mode(true);
    });
    routeapp.run(
    function($http) {
        //$http.defaults.headers.post['X-CSRFToken'] = $.cookie('csrftoken');
        // Add the following two lines
        $http.defaults.xsrfCookieName = 'csrftoken';
        $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    });

var app = angular.module('MyApp', ['angularUtils.directives.dirPagination', 'ngResource','ipCookie','ui.select2','ui.bootstrap','ui.router','angular-md5','ui.ace','base64','ngFileUpload']);
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

angular.element(document).ready(function() {
            var addroute = document.getElementById("addroute");
            angular.bootstrap(addroute, ["MyApp", "RouteApp"]);

            var pureapp = document.getElementById("pureapp");
            angular.bootstrap(pureapp, ["MyApp"]);
});
