'use strict';

var angular = require( 'angular' );

var module = angular.module(
	'communityshare.services.authentication',
	[
		'ngResource',
		'communityshare.services.user',
		'communityshare.services.conversation',
	] );

module.factory(
	'activeUserLoader',
	[ 'SessionBase', function( SessionBase ) {
		return SessionBase.getActiveUserPromise;
	} ] );

module.factory(
	'SessionBase',
	[ '$q', function( $q ) {
		var SessionBase = {};
		var deferred;
		SessionBase.clearUser = function() {
			deferred = $q.defer();
			SessionBase.activeUser = undefined;
		};
		SessionBase.setUser = function( user ) {
			deferred.resolve( user );
			SessionBase.activeUser = user;
			if ( user ) {
				user.updateUnviewedConversations();
			}
		};
		SessionBase.getActiveUserPromise = function() {
			return deferred.promise;
		};
		SessionBase.clearUser();
		return SessionBase;
	} ] );

module.factory(
	'Session',
	[ 'SessionBase', 'Authenticator', function( SessionBase, Authenticator ) {
		Authenticator.authenticateFromCookie();
		return SessionBase;
	} ] );

module.factory(
	'Authenticator',
	[ '$q', '$http', 'User', 'SessionBase', 'Messages', '$cookies', '$cookieStore', function( $q, $http, User, SessionBase, Messages, $cookies, $cookieStore ) {
		var Authenticator = {};
		Authenticator.clean = function() {
			$http.defaults.headers.common.Authorization = '';
			$cookieStore.remove( 'apiKey' );
			SessionBase.clearUser();
			SessionBase.setUser( undefined );
		};
		Authenticator.setApiKey = function( key ) {
			$http.defaults.headers.common.Authorization =
				'Basic:api:' + key;
			$cookies.apiKey = key;
		};

		Authenticator.authenticateFromCookie = function() {
			if( ! $cookies.id || ! $cookies.apiKey ) {
				Authenticator.clean();
				return $q.reject( 'No cookie' );
			}
			Authenticator.setApiKey( $cookies.apiKey );
			User.get( $cookies.id )
				.then( function( user ) {
					SessionBase.setUser( user );
				} )
				.catch( function( message ) {
					SessionBase.setUser( undefined );
					throw message;
				} );
		};

		Authenticator.authenticateWithEmailAndPassword = function( email, password ) {
			$http.defaults.headers.common.Authorization = `Basic:${email}:${password}`;
			SessionBase.clearUser();
			return $http( {
				url: '/api/requestapikey',
				method: 'GET',
			} )
				.then( function( { data: { apiKey, user } } ) {
					const userObj = User.make( user );
					Authenticator.setApiKey( apiKey );
					$cookies.id = userObj.id;
					SessionBase.setUser( userObj );
				} )
				.catch( function() {
					SessionBase.setUser( undefined );
				} );
		};

		Authenticator.signUp = function( user, password ) {
			SessionBase.clearUser();
			return $http( {
				method: 'POST',
				url: '/api/usersignup',
				data: {
					'user': user.toData(),
					'password': password,
				},
			} )
				.then( function( { data: { data, apiKey } } ) {
					const user = User.make( data );
					Authenticator.setApiKey( apiKey );
					$cookies.id = user.id;
					if ( user.warningMessage ) {
						Messages.error( 'Failed to send email to confirm address.' );
					}
					SessionBase.setUser( user );
					return user;
				} )
				.catch( function( { data: { message } } ) {
					SessionBase.setUser( undefined );
					throw message;
				} );
		};

		Authenticator.requestResetPassword = function( email ) {
			var url = 'api/requestresetpassword/' + email;
			var deferred = $q.defer();
			var promise = $http( {
				url: url,
				method: 'GET',
			} );
			promise.then(
				function( response ) {
					deferred.resolve( response.data );
				},
				function( response ) {
					var message;
					if ( response.data && response.data.message ) {
						message = response.data.message;
					}
					deferred.reject( message );
				} );
			return deferred.promise;
		};

		Authenticator.requestConfirmEmail = function() {
			var deferred = $q.defer();
			var url = 'api/requestconfirmemail';
			var promise = $http( {
				url: url,
				method: 'GET',
			} );
			promise.then(
				function() {
					deferred.resolve( undefined );
				},
				function( response ) {
					var message = 'Failed to send email confirmation email';
					if ( response.data && response.data.message ) {
						message += ': ' + response.data.message;
					}
					response.reject( message );
				} );
			return deferred.promise;
		};

		Authenticator.confirmEmail = function( key ) {
			var deferred = $q.defer();
			var url = 'api/confirmemail';
			var promise = $http( {
				url: url,
				method: 'POST',
				data: {
					key: key,
				},
			} );
			SessionBase.clearUser();
			promise.then(
				function( response ) {
					var apiKey = response.data.apiKey;
					var user = new User( response.data.data );
					Authenticator.setApiKey( apiKey );
					SessionBase.setUser( user );
					deferred.resolve( user );
				},
				function( response ) {
					var message = '';
					if ( response.data && response.data.message ) {
						message = response.data.message;
					}
					deferred.reject( message );
				} );
			return deferred.promise;
		};

		Authenticator.resetPassword = function( key, password ) {
			var deferred = $q.defer();
			var url = 'api/resetpassword';
			var promise = $http( {
				url: url,
				method: 'POST',
				data: {
					key: key,
					password: password,
				},
			} );
			promise.then(
				function( response ) {
					deferred.resolve( response.data );
				},
				function( response ) {
					var message = '';
					if ( response.data && response.data.message ) {
						message = response.data.message;
					}
					deferred.reject( message );
				} );
			return deferred.promise;
		};
		return Authenticator;
	} ]
);

