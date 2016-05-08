routeapp.factory('Project_Item_Origin', ['$resource', function($resource) {
        return $resource('/release/project_item_origin_api/:id', {}, {
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
