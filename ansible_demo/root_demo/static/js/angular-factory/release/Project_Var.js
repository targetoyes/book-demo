routeapp.factory('Project_Var', ['$resource', function($resource) {
        return $resource('/release/project_var_api/:id', {}, {
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
