// delete in the furture
app.factory('AuthService', ['$resource',
function($resource) {
    return $resource(
        '/users/:action', ///:password',
        {action:'@action',
        },
        {
            login: {
                method:'post',
                params: {
                    action: 'login/',
                    username: '@username',
                    password: '@password',
                }   
            },  
            logout: {
                method:'post',
                params: {
                    action: 'logout/'
                }   
            }   
        }
    );
}]);
//

app.controller('LoginCtrl', function LoginCtrl($scope, $window, $http, ipCookie, md5) {
    $scope.release_login = function() {
        $scope.password =  md5.createHash($scope.password);
        $http.post('/users/login/',
        {'username': $scope.username,'password': $scope.password}
        ).success(function(res){
            $scope.message = 'now login';
            ipCookie('loginname', $scope.username, {path: '/'});
            ipCookie('password', $scope.password, {path: '/'});
            $window.location.href = "/release/mainpage";
        }).error(function(err){
            $scope.message = "password error or loginname not exists!"
            alert($scope.message);
            ipCookie.remove('loginname', {path: '/'});
            ipCookie.remove('password', {path: '/'});
            $window.location.href = "/login";
        });     
    };   
});
