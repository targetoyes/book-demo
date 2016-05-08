routeapp.factory('Family', ['$resource', function($resource) {
        return $resource('/auth_control/family_api/:id', {}, {
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
            put: {
                method: 'PUT'
                },
                });
}]);            
