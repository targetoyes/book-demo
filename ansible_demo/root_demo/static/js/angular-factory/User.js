app.factory('User', ['$resource', function($resource) {
        return $resource('/users/:id', {},
                {
                    query: { 
                        method: 'GET',
                        //params: { action: "username" },
                        isArray: true ,
                    },
                    save: {
                        method: 'POST'
                    },
                    remove: {
                        method: 'DELTET'
                    },
                });
}]);        


