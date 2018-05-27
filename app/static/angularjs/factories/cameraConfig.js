(function (){
	'use strict';

	angular.module('RecognitionApp').factory('cameraConfig', function($http, $localStorage){
		
		var _setCam = function(){
			if($localStorage.camera!=undefined){
				if($localStorage.camera.type=='local'){
					$localStorage.camera={};
					$localStorage.camera.type='local'
				}
			}
			return $http.post('/add_cam', $localStorage.camera)
		};

		return{
			setCam: _setCam
		}
	})
})();