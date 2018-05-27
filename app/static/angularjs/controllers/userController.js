(function(){
	
	'use strict';

	angular.module('RecognitionApp').controller('UserController', function($scope, $http, $log, $location, $localStorage, $timeout, cameraConfig){
		
		var self=this

		self.user=undefined
		$scope.imageFaces=[];
		self.activeVideo=undefined;

		cameraConfig.setCam().success(function(results){
			$log.log(results)
		})

		self.adjustPathFace = function(faces){
			var newFaces=[]
			for (var i=0; i<faces.length; i++){
				var image = new Image();
				image.src = 'data:image/jpg;base64,'+faces[i];
				newFaces.unshift(image);
			}
			return newFaces;
		}

		self.loadFaces = function(){
			$http.post('/load_faces', self.user.id)
			.success(function(results){
				$scope.imageFaces=self.adjustPathFace(results.faces);
			}).error(function(error){
				$log.log(error);
			})
		}

		self.loadUser = function(){
			if($localStorage.user!=undefined){
				self.user=$localStorage.user
				self.loadFaces()
			}
		}

		self.loadUser();


		self.addImage = function(){
			
			self.activeVideo=false;
			$timeout( function(){ 
				$http.post('/add_image').
				success(function(results){
					var image = new Image();
					var url_image=results.image_face.substr(1,(results.image_face.length - 2));
					image.src = 'data:image/png;base64,'+url_image;
					$scope.imageFaces.unshift(image)
					self.startVideo();
				}).
				error(function(error){
					$log.log(error)
				})
			}, 1000);
			
		}

		self.removeImage = function(){
			
			self.activeVideo=false;
			$timeout( function(){ 
				$http.post('/remove_image').
				success(function(results){
					$scope.imageFaces.shift();
					self.startVideo();
				}).
				error(function(error){
					$log.log(error)
				})
			}, 1000);
		}

		self.submit = function(){
			if(self.user!=undefined && self.user.id==undefined)
				self.saveUser();
			else if(self.user.id!=undefined)
				self.editUser();
		}

		self.cleanVideo = function(){
			self.activeVideo=false;
		}

		self.saveUser = function(){
			self.cleanVideo();
			$http.post('/save_user', self.user).
			success(function(results){
				self.user=undefined;
				self.activeVideo=undefined;
				alert('Seu identificador é: ' + results.id);
				$location.path('/');
			}).
			error(function(error){
				$log.log(error)
			})
		}

		self.editUser = function(){
			self.cleanVideo();
			$http.post('/edit_user', self.user).
			success(function(results){
				self.user=undefined;
				$location.path('/');
			}).
			error(function(error){
				$log.log(error)
			})
		}

		self.startVideo = function(){
			self.activeVideo=true;
		}

		self.deleteUser = function(){
			self.cleanVideo();
			$http.delete('/delete_user/'+ self.user.id).
			success(function(results){
				self.user=undefined
				$location.path('/')
			}).
			error(function(error){
				$log.log(error)
			})
		}

	})


})()