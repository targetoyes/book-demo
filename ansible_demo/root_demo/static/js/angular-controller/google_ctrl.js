app.controller('google_ctrl',function($scope){
    $scope.search = '';
    $scope.$watch('search',function() {
        $scope.gosearch = $scope.search.split(' ').join('+');
        $scope.googleurl = 'http://gl.randomk.org/search?q=' + $scope.gosearch + '&btnG=Google+搜索';
        $scope.stackoverflowurl = 'http://stackoverflow.com/search?q=' + $scope.gosearch;
        $scope.searchcodeurl = 'https://searchcode.com/?q=' + $scope.gosearch;
        });
});
