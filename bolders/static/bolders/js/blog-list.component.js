'use strict';

angular.module('blogList').
//    controller('BlogListController', function($scope){
//        console.log('hi')
//        $scope.title = 'hi there'
//    });
    component('blogList', {
        template: "<div><h1>{{ title }}</h1><button ng-click='someClickTest()'>Click</button></div>",
        //templateUrl: "static/bolders/js/templates/ng-list.html",
        controller: function($scope){
            $scope.clicks = 0
            $scope.title = 'Clicked ' + $scope.clicks + ' times.'
            $scope.someClickTest = function(){
                $scope.clicks += 1
                $scope.title = 'Clicked ' + $scope.clicks + ' times.'
            }
        }
    });
