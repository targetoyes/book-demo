routeapp.factory('Database_Conn', ['$resource', function($resource) {
        return $resource('/release/database_conn_api/:id', {}, {
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
