routeapp.factory('Project_Item', ['$resource', function($resource) {
        return $resource('/release/project_item_api/:id', {}, {
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
