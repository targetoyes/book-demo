routeapp.directive("diaCheck", function($timeout) {                                                  
    return {                                                                                 
        restrict: 'E',                                                                       
        transclude: true,                                                                    
        scope: {                                                                             
            modelmsg: '=',
            modeltitle: '=',
            modelbody: '=',
            callbackbuttonleft: '&ngClickLeft',                                              
            callbackbuttonright: '&ngClickRight'                                             
        },                                                                                   
        link: function(scope, element, attrs) {                                              
            scope.dia_name = attrs.diaName;                                                  
            if(angular.isUndefined(attrs.diaSize)){                                          
                scope.dia_size = '';                                                         
            }else{                                                                           
                if(attrs.diaSize == 'S' || attrs.diaSize == 's'){                            
                    scope.dia_size = 'model-sm';                                             
                };                                                                           
                if(attrs.diaSize == 'L' || attrs.diaSize == 'l'){                            
                    scope.dia_size = 'modal-lg';                                             
                }else{                                                                       
                    scope.dia_size = '';                                                     
                };                                                                           
            };                                                                               
            if(angular.isUndefined(attrs.diaTitle)){                                            
                scope.dia_title = '提示';                                                        
            }else{                                                                           
                scope.dia_title = attrs.diaTitle;                                                   
            };                                                                               
            if(angular.isUndefined(attrs.diaBody)){                                             
                scope.dia_body = '确认提交数据,数据将被修改';                                    
            }else{                                                                           
                scope.dia_body = attrs.diaBody;                                                     
            };                                                                               
        },                                                                                   
        template: 
    '<div class="modal fade" id="((dia_name))" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">'+            
        '<div class="modal-dialog ((dia_size))">'+                                                                                         
            '<div class="modal-content">'+                                                                                                 
                '<div class="modal-header">'+                                                                                              
                    '<button type="button" class="close" data-dismiss="modal" aria-label="Close">'+                                        
                        '<span aria-hidden="true">&times;</span>'+                                                                         
                    '</button>'+
                    '<h4 class="modal-title" ng-if="dia_title">'+
                        '((dia_title))'+
                    '</h4>'+                                                                     
                    '<h4 class="modal-title" ng-if="modeltitle">'+
                        '((modeltitle))'+
                    '</h4>'+                                                                     
                '</div>'+                                                                                                                  
                '<div class="modal-body">'+                                                                                                
                    '<p ng-if="dia_body">((dia_body))</p>'+
                    '<p ng-if="modelbody">((modelbody))</p>'+                                                                                                     
                '</div>'+                                                                                                                  
                '<div class="modal-footer">'+                                                                                              
                    '<button id="holder" type="button" class="btn btn-primary" data-dismiss="modal" ng-click="callbackbuttonleft()">确认</button>'+                                                                                                         
                    '<button type="button" class="btn btn-default" data-dismiss="modal" ng-click="callbackbuttonright()">取消</button>'+   
                    '<div class="col-md-12">'+
                        '<h5>((modelmsg))</h5>'+
                    '</div>'+
                '</div>'+                                                                                                                  
            '</div>'+                                                                                                                      
        '</div>'+                                                                                                                          
    '</div>',                                                                                                                              
    }
});
//<button type="submit" class="btn btn btn-primary col-md-offset-5" data-toggle="modal" data-target="#psps">提交</button>

//<dia-check dia_name='psps' dia_size='L' dia_title='check_list' dia_body='test'>
