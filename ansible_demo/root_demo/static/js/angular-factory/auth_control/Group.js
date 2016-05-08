routeapp.factory('Group', ['$resource', function($resource) {
        return $resource('/groups/:id', {}, {
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
