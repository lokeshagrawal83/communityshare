var path = require( 'path' );
var webpack = require( 'webpack' );
var ExtractTextPlugin = require( 'extract-text-webpack-plugin' );
var ManifestPlugin = require( 'manifest-revision-webpack-plugin' );

module.exports = {
    entry: {
        bundle: path.join( __dirname, 'static', 'js', 'index.js' ),
        vendor: [
            'angular',
            'angular-animate',
            'angular-cookies',
            'angular-resource',
            'angular-route',
            'error-stack-parser',
            'jquery'
        ]
    },
    module: {
        loaders: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loaders: [ 'ng-annotate' ]
            },
            {
                test: /\.css$/,
                loader: ExtractTextPlugin.extract( 'style-loader', 'css-loader' )
            },
            {
                test: /\.(eot|svg|ttf|woff|woff2)$/,
                loader: 'file?name=static/fonts/[name].[ext]'
            }
        ]
    },
    plugins: [
        new ManifestPlugin( 'manifest.json', {
            rootAssetPath: './static/build/',
            ignorePaths: [ /\.map$/ ],
            extensionsRegex: /\.js$/
        } ),
        new ExtractTextPlugin( 'bundle.[chunkhash].css', { allChunks: true } ),
        new webpack.optimize.CommonsChunkPlugin( 'vendor', 'vendor.bundle.[chunkhash].js' ),
        new webpack.ProvidePlugin( {
           $: 'jquery'
        } )
    ],
    output: {
        path: path.join( __dirname, 'static', 'build' ),
        filename: '[name].[chunkhash].js'
    },
    devtool: 'source-map',
    // needed because we won't get inotify/fsevents
    // inside of the Docker images
    watchOptions: {
      poll: true
    }
};

