'use strict';
var requirements, app;

requirements = [
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
if ( !window.history.replaceState ) {
    requirements.push( 'ng.shims.placeholder' );
}

app = angular.module( 'communityshare', requirements );

app.config( ['$routeProvider', function ( $routeProvider ) {

    $routeProvider.when( '/', {
        templateUrl: './static/templates/default.html',
        controller: 'DefaultController',
        resolve: {
            user: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }]
        }
    } );

    $routeProvider.when( '/signup/choice', {
        templateUrl: './static/templates/choose_user_type.html'
    } );

    $routeProvider.when( '/login', {
        templateUrl: './static/templates/login.html',
        controller: 'LoginController'
    } );

    $routeProvider.when( '/signup/communitypartner', {
        templateUrl: './static/templates/signup_community_partner.html',
        controller: 'SignupCommunityPartnerController',
        resolve: {
            user: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }]
        }
    } );

    $routeProvider.when( '/signup/personal', {
        templateUrl: './static/templates/signup_personal.html',
        controller: 'SignupPersonalController',
        resolve: {
            user: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }]
        }
    } );

    $routeProvider.when( '/signup/educator', {
        templateUrl: './static/templates/signup_educator.html',
        controller: 'SignupEducatorController',
        resolve: {
            user: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }]
        }
    } );

    $routeProvider.when( '/requestresetpassword', {
        templateUrl: './static/templates/request_reset_password.html',
        controller: 'RequestResetPasswordController'
    } );

    $routeProvider.when( '/resetpassword', {
        templateUrl: './static/templates/reset_password.html',
        controller: 'ResetPasswordController'
    } );

    $routeProvider.when( '/confirmemail', {
        templateUrl: './static/templates/confirm_email.html',
        controller: 'ConfirmEmailController'
    } );

    $routeProvider.when( '/settings', {
        templateUrl: './static/templates/settings.html',
        controller: 'SettingsController',
        resolve: {
            activeUser: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }]
        }
    } );

    $routeProvider.when( '/messages', {
        templateUrl: './static/templates/messages.html',
        controller: 'MessagesController',
        resolve: {
            activeUser: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }]
        }
    } );

    $routeProvider.when( '/shares', {
        templateUrl: './static/templates/shares.html',
        controller: 'SharesController',
        resolve: {
            activeUser: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }]
        }
    } );

    $routeProvider.when( '/user/:userId', {
        templateUrl: './static/templates/user_view.html',
        controller: 'UserController',
        resolve: {
            activeUser: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }]
        }
    } );

    $routeProvider.when( '/search/:searchId/edit', {
        templateUrl: './static/templates/search_edit.html',
        controller: 'SearchEditController',
        resolve: {
            activeUser: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }]
        }
    } );

    $routeProvider.when( '/searchusers/:searchText', {
        templateUrl: './static/templates/search_users.html',
        controller: 'SearchUsersController',
        resolve: {
            activeUser: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }]
        }
    } );

    $routeProvider.when( '/searchusers', {
        templateUrl: './static/templates/search_users.html',
        controller: 'SearchUsersController',
        resolve: {
            activeUser: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }]
        }
    } );

    $routeProvider.when( '/matches', {
        templateUrl: './static/templates/matches.html',
        controller: 'MatchesController',
        resolve: {
            activeUser: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }]
        }
    } );

    $routeProvider.when( '/admin', {
        templateUrl: './static/templates/admin.html',
        controller: 'AdminController',
        resolve: {
            activeUser: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }]
        }
    } );


    $routeProvider.when( '/search/:searchId/results', {
        templateUrl: './static/templates/search_results.html',
        controller: 'SearchResultsController',
        resolve: {
            activeUser: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }]
        }
    } );

    $routeProvider.when( '/search', {
        templateUrl: './static/templates/search.html',
        controller: 'SearchEditController',
        resolve: {
            activeUser: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }]
        }
    } );

    $routeProvider.when( '/conversation/unviewed', {
        templateUrl: './static/templates/unviewed_conversations.html',
        controller: 'UnviewedConversationController',
        resolve: {
            activeUser: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }]
        }
    } );

    $routeProvider.when( '/events', {
        templateUrl: './static/templates/events.html',
        controller: 'EventsController',
        resolve: {
            activeUser: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }]
        }
    } );

    $routeProvider.when( '/event/:eventId', {
        templateUrl: './static/templates/event_view.html',
        controller: 'EventController',
        resolve: {
            activeUser: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }],
            evnt: ['eventLoader', '$route', function ( eventLoader, $route ) {
                return eventLoader( $route.current.params.eventId );
            }]
        }
    } );

    $routeProvider.when( '/conversation/:conversationId', {
        templateUrl: './static/templates/conversation.html',
        controller: 'ConversationController',
        resolve: {
            activeUser: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }],
            conversation: ['conversationLoader', '$route', function ( conversationLoader, $route ) {
                return conversationLoader( $route.current.params.conversationId );
            }]
        }
    } );

    $routeProvider.when( '/share/new', {
        templateUrl: './static/templates/share_edit.html',
        controller: 'NewShareController',
        resolve: {
            activeUser: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }]
        }
    } );

    $routeProvider.when( '/share/:shareId', {
        templateUrl: './static/templates/share.html',
        controller: 'ShareController',
        resolve: {
            activeUser: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }]
        }
    } );

    $routeProvider.when( '/auth_redirect', {
        templateUrl: './static/templates/auth_redirect.html',
        controller: 'AuthRedirectController',
        resolve: {
            activeUser: ['activeUserLoader', function ( activeUserLoader ) {
                return activeUserLoader();
            }]
        }
    } );

    $routeProvider.otherwise( {
        templateUrl: './static/templates/unknown.html'
    } );
}] );

//http://stackoverflow.com/questions/16098430/angular-ie-caching-issue-for-http
app.config( ['$httpProvider', function ( $httpProvider ) {
    //initialize get if not there
    if ( !$httpProvider.defaults.headers.get ) {
        $httpProvider.defaults.headers.get = {};
    }
    //disable IE ajax request caching
    $httpProvider.defaults.headers.get['If-Modified-Since'] = '0';
}] );

// Patch .indexOf() for IE8
// http://stackoverflow.com/questions/3629183/why-doesnt-indexof-work-on-an-array-ie8
if ( !Array.prototype.indexOf ) {
    Array.prototype.indexOf = function ( elt ) {
        var len
            , from
            ;

        len = this.length >>> 0;
        from = Number( arguments[1] ) || 0;
        from = ( from < 0 ) ? Math.ceil( from ) : Math.floor( from );

        if ( from < 0 ) from += len;

        for ( ; from < len; from++ ) {
            if ( from in this && this[from] === elt ) return from;
        }

        return -1;
    };
}

// Provide String.trim() poly-fill for IE8
if ( typeof String.prototype.trim !== 'function' ) {
    String.prototype.trim = function () {
        return this.replace( /^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, '' );
    };
}

window.console = window.console || {};

Date.now = Date.now || function () {
    return +new Date;
};

