'use strict';

var angular = require( 'angular' );

var module = angular.module( 'communityshare.controllers.message', ['ngAnimate'] );

module.controller(
'MessageController',
['$scope', 'Messages', function ( $scope, Messages ) {
    $scope.messages = Messages;
}] );

