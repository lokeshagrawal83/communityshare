/* eslint-env node */

var path = require( 'path' );
var ExtractTextPlugin = require( 'extract-text-webpack-plugin' );
var ManifestPlugin = require( 'manifest-revision-webpack-plugin' );

var bundleHash = process.env.NODE_ENV === 'production' ? '.[chunkhash]' : '';

module.exports = {
	entry: {
		bundle: path.join( __dirname, 'static', 'js', 'index.js' ),
	},
	externals: [ {
		angular: true,
	} ],
	module: {
		loaders: [
			{
				test: /\.js$/,
				exclude: /node_modules/,
				loaders: [ 'ng-annotate', 'babel' ],
			},
			{
				test: /\.css$/,
				loader: ExtractTextPlugin.extract( 'style-loader', 'css-loader' ),
			},
			{
				test: /\.(eot|svg|ttf|woff|woff2)$/,
				loader: 'file?name=static/fonts/[name].[ext]',
			},
		],
	},
	plugins: [
		new ManifestPlugin( 'manifest.json', {
			rootAssetPath: './static/build/',
			ignorePaths: [ /\.map$/ ],
			extensionsRegex: /\.js$/,
		} ),
		new ExtractTextPlugin( 'bundle' + bundleHash + '.css', { allChunks: true } ),
	],
	output: {
		path: path.join( __dirname, 'static', 'build' ),
		filename: '[name]' + bundleHash + '.js',
	},
	devtool: 'source-map',
	// needed because we won't get inotify/fsevents
	// inside of the Docker images
	watchOptions: {
		poll: true,
	},
};

