(function(){
	
	'use strict';

	angular.module('RecognitionApp').controller('RecognizerController', function($scope, $log, cameraConfig, $timeout){
		
		var self=this;

		self.activeRecognizer=undefined;

		cameraConfig.setCam().success(function(results){
			$log.log(results)
		})

		self.startRecognizer = function(){
			self.activeRecognizer=false;
			$timeout( function(){
				self.activeRecognizer=true;
			}, 100);	
		}

		self.stopRecognizer = function(){
			self.activeRecognizer=undefined;
		}
	})

})()