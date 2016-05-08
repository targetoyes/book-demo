app.controller('CookieCtrl', function ($scope, $window, $location, $rootScope, ipCookie, $http, User) {
    loginname = ipCookie('loginname');
    $scope.login_exist = ipCookie('loginname');
    token = ipCookie('token');
    if (!loginname || !token){
        $scope.loginname = 'welcome to login';
    }else
    {
        $http.post('/release/auth_api/login_vaild/',
                    {'username': loginname,'token': token}
        ).success(function(result){
            $scope.loginname = ipCookie('loginname');
            $scope.message = 'check user ok';
        }).error(function(err){
            $scope.message = "please login!"
            alert($scope.message);
            ipCookie.remove('loginname', {path: '/'});
            $scope.loginname = 'welcome to login';
            ipCookie.remove('token', {path: '/'});
        });
    };

    if (!loginname){
        $scope.log_value = 'login';
        }
    else{ 
        $scope.log_value = 'logout';
    };
    
    $scope.comeback_mainpage_func = function(){         
        $window.location.href = "/release/mainpage";    
    };                                                  

    $scope.comeback_change_pass_func = function(){      
        $window.location.href = "/change_pass";
    };                                                  

    $scope.comeback_register_func = function(){      
        $window.location.href = "/register";
    };                                                  

    $scope.log_redirect = function(){
        if ($scope.log_value == 'login'){$window.location.href = "/login";};
        if ($scope.log_value == 'logout'){
            ipCookie.remove('loginname', {path: '/'});
            ipCookie.remove('token', {path: '/'});
            $window.location.href = "/login";
        };
    };

});

