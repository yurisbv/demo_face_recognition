(function(){
	
	'use strict';

	angular.module('RecognitionApp').config(function($routeProvider, $locationProvider) {
	    
		$locationProvider.html5Mode({
  			enabled: true,
  			requireBase: false
		});


	    $routeProvider

	    .when("/", {
	        templateUrl : "/static/pages/home.html",
	        controller: 'IndexController',
	        controllerAs: 'ic'
	    })

	    .when("/recognition", {
	        templateUrl : "/static/pages/recognition.html",
	        controller: 'RecognizerController',
	        controllerAs: 'rc'
	    })

	    .when("/register", {
	        templateUrl : "/static/pages/user.html",
	        controller: 'UserController',
	        controllerAs:'uc'
	    })

	    .when("/configuration", {
	    	templateUrl:"/static/pages/configuration.html",
	    	controller:'ConfigController',
	    	controllerAs: 'cc'
	    })

	    .when("/edit", {
	    	templateUrl: "/static/pages/user.html",
	    	controller:'UserController',
	    	controllerAs:'uc'
	    });
	});
})();