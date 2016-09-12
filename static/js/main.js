const requirements = [
	'ngRoute',
	'ui.bootstrap',
	'communityshare.directives.mainview',
	'communityshare.controllers.authentication',
	'communityshare.controllers.misc',
	'communityshare.controllers.user',
	'communityshare.controllers.search',
	'communityshare.controllers.message',
	'communityshare.controllers.share',
	'communityshare.directives.labels',
	'communityshare.services.share'
];

// Use placeholder shim if browser doesn't support html5
if ( ! window.history.replaceState ) {
	requirements.push( 'ng.shims.placeholder' );
}

const app = angular.module( 'communityshare', requirements );

const invoker = f => f();
const requireLogin = { user: [ 'activeUserLoader', invoker ] };

const routes = [
	[ '/', {
		templateUrl: './static/templates/default.html',
		controller: 'DefaultController',
		resolve: requireLogin
	} ],

	[ '/signup/choice', {
		templateUrl: './static/templates/choose_user_type.html'
	} ],

	[ '/login', {
		templateUrl: './static/templates/login.html',
		controller: 'LoginController'
	} ],

	[ '/signup/communitypartner', {
		templateUrl: './static/templates/signup_community_partner.html',
		controller: 'SignupCommunityPartnerController',
		resolve: requireLogin
	} ],

	[ '/signup/personal', {
		templateUrl: './static/templates/signup_personal.html',
		controller: 'SignupPersonalController',
		resolve: requireLogin
	} ],

	[ '/signup/educator', {
		templateUrl: './static/templates/signup_educator.html',
		controller: 'SignupEducatorController',
		resolve: requireLogin
	} ],

	[ '/requestresetpassword', {
		templateUrl: './static/templates/request_reset_password.html',
		controller: 'RequestResetPasswordController'
	} ],

	[ '/resetpassword', {
		templateUrl: './static/templates/reset_password.html',
		controller: 'ResetPasswordController'
	} ],

	[ '/confirmemail', {
		templateUrl: './static/templates/confirm_email.html',
		controller: 'ConfirmEmailController'
	} ],

	[ '/settings', {
		templateUrl: './static/templates/settings.html',
		controller: 'SettingsController',
		resolve: requireLogin
	} ],

	[ '/messages', {
		templateUrl: './static/templates/messages.html',
		controller: 'MessagesController',
		resolve: requireLogin
	} ],

	[ '/shares', {
		templateUrl: './static/templates/shares.html',
		controller: 'SharesController',
		resolve: requireLogin
	} ],

	[ '/user/:userId', {
		templateUrl: './static/templates/user_view.html',
		controller: 'UserController',
		resolve: requireLogin
	} ],

	[ '/search/:searchId/edit', {
		templateUrl: './static/templates/search_edit.html',
		controller: 'SearchEditController',
		resolve: requireLogin
	} ],

	[ '/searchusers/:searchText', {
		templateUrl: './static/templates/search_users.html',
		controller: 'SearchUsersController',
		resolve: requireLogin
	} ],

	[ '/searchusers', {
		templateUrl: './static/templates/search_users.html',
		controller: 'SearchUsersController',
		resolve: requireLogin
	} ],

	[ '/matches', {
		templateUrl: './static/templates/matches.html',
		controller: 'MatchesController',
		resolve: requireLogin
	} ],

	[ '/admin', {
		templateUrl: './static/templates/admin.html',
		controller: 'AdminController',
		resolve: requireLogin
	} ],

	[ '/search/:searchId/results', {
		templateUrl: './static/templates/search_results.html',
		controller: 'SearchResultsController',
		resolve: requireLogin
	} ],

	[ '/search', {
		templateUrl: './static/templates/search.html',
		controller: 'SearchEditController',
		resolve: requireLogin
	} ],

	[ '/conversation/unviewed', {
		templateUrl: './static/templates/unviewed_conversations.html',
		controller: 'UnviewedConversationController',
		resolve: requireLogin
	} ],

	[ '/events', {
		templateUrl: './static/templates/events.html',
		controller: 'EventsController',
		resolve: requireLogin
	} ],

	[ '/event/:eventId', {
		templateUrl: './static/templates/event_view.html',
		controller: 'EventController',
		resolve: {
			activeUser: [ 'activeUserLoader', invoker ],
			evnt: [ 'eventLoader', '$route', function( eventLoader, $route ) {
				return eventLoader( $route.current.params.eventId );
			} ]
		}
	} ],

	[ '/conversation/:conversationId', {
		templateUrl: './static/templates/conversation.html',
		controller: 'ConversationController',
		resolve: {
			activeUser: [ 'activeUserLoader', invoker ],
			conversation: [ 'conversationLoader', '$route', function( conversationLoader, $route ) {
				return conversationLoader( $route.current.params.conversationId );
			} ]
		}
	} ],

	[ '/share/new', {
		templateUrl: './static/templates/share_edit.html',
		controller: 'NewShareController',
		resolve: requireLogin
	} ],

	[ '/share/:shareId', {
		templateUrl: './static/templates/share.html',
		controller: 'ShareController',
		resolve: requireLogin
	} ],

	[ '/auth_redirect', {
		templateUrl: './static/templates/auth_redirect.html',
		controller: 'AuthRedirectController',
		resolve: requireLogin
	} ]
];

app.config( [ '$routeProvider', function( $routeProvider ) {
	routes.forEach(
		( [ path, route ] ) => $routeProvider.when( path, route )
	);

	$routeProvider.otherwise( {
		templateUrl: './static/templates/unknown.html'
	} );
} ] );

//http://stackoverflow.com/questions/16098430/angular-ie-caching-issue-for-http
app.config( [ '$httpProvider', function( $httpProvider ) {
	//initialize get if not there
	if ( ! $httpProvider.defaults.headers.get ) {
		$httpProvider.defaults.headers.get = {};
	}

	//disable IE ajax request caching
	$httpProvider.defaults.headers.get[ 'If-Modified-Since' ] = '0';
} ] );

// From MDN
// Production steps of ECMA-262, Edition 5, 15.4.4.14
// Reference: http://es5.github.io/#x15.4.4.14
if ( ! Array.prototype.indexOf ) {
	Array.prototype.indexOf = function( searchElement, fromIndex ) {

		var k;

		// 1. Let o be the result of calling ToObject passing
		//    the this value as the argument.
		if ( this == null ) {
			throw new TypeError( '"this" is null or not defined' );
		}

		var o = Object( this );

		// 2. Let lenValue be the result of calling the Get
		//    internal method of o with the argument "length".
		// 3. Let len be ToUint32(lenValue).
		var len = o.length >>> 0;

		// 4. If len is 0, return -1.
		if ( len === 0 ) {
			return - 1;
		}

		// 5. If argument fromIndex was passed let n be
		//    ToInteger(fromIndex); else let n be 0.
		var n = + fromIndex || 0;

		if ( Math.abs( n ) === Infinity ) {
			n = 0;
		}

		// 6. If n >= len, return -1.
		if ( n >= len ) {
			return - 1;
		}

		// 7. If n >= 0, then Let k be n.
		// 8. Else, n<0, Let k be len - abs(n).
		//    If k is less than 0, then let k be 0.
		k = Math.max( n >= 0 ? n : len - Math.abs( n ), 0 );

		// 9. Repeat, while k < len
		while ( k < len ) {
			// a. Let Pk be ToString(k).
			//   This is implicit for LHS operands of the in operator
			// b. Let kPresent be the result of calling the
			//    HasProperty internal method of o with argument Pk.
			//   This step can be combined with c
			// c. If kPresent is true, then
			//    i.  Let elementK be the result of calling the Get
			//        internal method of o with the argument ToString(k).
			//   ii.  Let same be the result of applying the
			//        Strict Equality Comparison Algorithm to
			//        searchElement and elementK.
			//  iii.  If same is true, return k.
			if ( k in o && o[ k ] === searchElement ) {
				return k;
			}
			k ++;
		}
		return - 1;
	};
}

// From MDN
if ( ! String.prototype.trim ) {
	String.prototype.trim = function() {
		return this.replace( /^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, '' );
	};
}

window.console = window.console || {};

// From MDN
if ( ! Date.now ) {
	Date.now = function now() {
		return new Date().getTime();
	};
}

