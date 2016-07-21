var path = require( 'path' );
var webpack = require( 'webpack' );
var ManifestPlugin = require( 'manifest-revision-webpack-plugin' );

module.exports = {
    entry: {
        bundle: path.join( __dirname, 'static', 'js', 'index.js' )
    },
    externals: [ {
        angular: true
    } ],
    module: {
        loaders: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loaders: [ 'ng-annotate' ]
            }
        ]
    },
    plugins: [
        new ManifestPlugin( 'manifest.json', {
            rootAssetPath: './static/build/',
            ignorePaths: [ /\.map$/ ],
            extensionsRegex: /\.js$/
        } )
    ],
    output: {
        path: path.join( __dirname, 'static', 'build' ),
        filename: '[name].[hash].js'
    },
    devtool: 'source-map'
};

