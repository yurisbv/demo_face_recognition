(function(){
	
	'use strict';

	angular.module('RecognitionApp').controller('ConfigController', function($http, $log, $localStorage){
		
		var self = this;

		self.camera={};

		self.validatePlaceHolder = function(){
			if(self.camera.ip==undefined || self.camera.ip == ''){
				self.camera.ip = '';
			}

		}

		self.setCam = function(){
			$http.get('/set_cam').
			success(function(results){
				self.camera.type=results.cameraType;
				self.camera.ip=results.cameraIp;
				self.camera.port=results.cameraPort;
				self.camera.url=results.cameraUrl;
				if(self.camera.type!='local')
					$localStorage.camera=self.camera;
				else
					delete $localStorage.camera
			
			}).
			error(function(error){
				$log.log(error)
			})
		}
		self.setCam()

		self.saveCam = function(){
			$http.post('/save_cam', self.camera).
			success(function(results){
				$log.log(results)
				if(results.status=='True'){
					self.camera.url=results.cameraUrl;
					$localStorage.camera=self.camera;
					alert('Câmera configurada com sucesso!')
				}else{
					alert('Erro ao configurar câmera')
					self.camera={};
					self.camera.type='local'
					delete $localStorage.camera
				}
			}).
			error(function(error){
				$log.log(error)
			})
		}

	})

})()