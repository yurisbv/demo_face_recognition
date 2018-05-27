(function(){
	
	'use strict'

	angular.module('RecognitionApp').directive("rgBreadcrumb", function(){


		return{
			templateUrl: '/static/angularjs/directiveView/breadcrumb.html',
			restrict: 'AE',
			scope: {
				titlepage: "@"
			},
			controller:'IndexController'
		}
	})


})()