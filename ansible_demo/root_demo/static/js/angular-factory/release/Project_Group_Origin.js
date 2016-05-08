routeapp.factory('Project_Group_Origin', ['$resource', function($resource) {
        return $resource('/release/project_group_origin_api/:id', {}, {
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
