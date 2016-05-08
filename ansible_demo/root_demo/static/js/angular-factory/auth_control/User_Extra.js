routeapp.factory('User_Extra', ['$resource', function($resource) {
        return $resource('/release/auth_api/:id', {}, {
            query:{
                method: 'GET',
                 //cache: true,
                isArray: true
                },
            save: {
                method: 'POST'
                },
            remove: {
                method: 'DELTET'
                },
                });
}]);            
