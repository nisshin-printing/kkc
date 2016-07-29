var gulp        = require('gulp'),
	$           = require('gulp-load-plugins')(),
	imagePng    = require('imagemin-pngquant'),
	browserSync = require('browser-sync');

var path = {
	css: './assets/css/',
	sass: './assets/sass/',
	js: './assets/js/',
	precom: './assets/js/pre-compress/',
	src: './assets/js/src/',
	admin_src: './assets/js/admin/',
	img: './assets/img/',
	svg: './assets/svg/',
	svgIcons: './assets/svg/icons/',
};

/* =========================================  タスク  ================================ */
// $.compass
// Main CSS
gulp.task('style', function() {
	gulp.src([path.sass + '**/*.scss', '!' + path.sass + '**/_*.scss'])
		.pipe($.plumber({
		errorHandler: $.notify.onError('Error: <%= error.message %>')
	}))
		.pipe($.sass({
		config_file: './config.rb',
		css: path.css,
		sass: path.sass,
		image: path.img,
		javascript: path.js,
		comments: true
	}))
		.pipe($.autoprefixer())
		.pipe($.cssmin())
		.pipe(gulp.dest( path.css ))
		.pipe(browserSync.reload({ stream: true }));
});

// SVG Icons & Images
// SVG
gulp.task('svg', function() {
	gulp.src( path.svgIcons + '*.svg')
		.pipe( $.plumber({
		errorHandler: function(error) {
			console.log(error.messageFormatted);
			this.emit('end');
		}
	}))
		.pipe($.svgmin())
		.pipe($.svgstore({ inlineSvg: true }))
		.pipe($.cheerio({
		run: function ($) {
			$('svg').addClass('test');
			$('[fill]').removeAttr('fill');
		},
		parserOptions: { xmlMode: true }
	}))
		.pipe(gulp.dest(path.svg))
		.pipe(browserSync.reload({ stream: true }));
});
gulp.task('svg2png', function() {
	gulp.src(path.svgIcons + '*.svg')
		.pipe( $.plumber({
		errorHandler: function(error) {
			console.log(error.messageFormatted);
			this.emit('end');
		}
	}))
		.pipe($.svg2png())
		.pipe($.rename({
		prefix: 'icons.svg.'
	}))
		.pipe(gulp.dest(path.svg))
		.pipe(browserSync.reload({ stream: true }));
});

// JAVASCRIPT
// For inline scripts
gulp.task('precom-scripts', function() {
	gulp.src( path.precom + '*.js')
		.pipe($.plumber({
		errorHandler: $.notify.onError('Error: <%= error.message %>')
	}))
		.pipe($.uglify())
		.pipe($.rename({
		extname: '.min.js'
	}))
		.pipe(gulp.dest( path.js ))
		.pipe(browserSync.reload({ stream: true }));
});
gulp.task('plugin-precom', function() {
	gulp.src( plugin.precom + '*.js')
		.pipe($.plumber({
		errorHandler: $.notify.onError('Error: <%= error.message %>')
	}))
		.pipe($.uglify())
		.pipe($.rename({
		extname: '.min.js'
	}))
		.pipe(gulp.dest( plugin.js ))
		.pipe(browserSync.reload({ stream: true }));
});
// Main path.App Javascript
gulp.task('src-js', function() {
	gulp.src( path.src + '*.js')
		.pipe($.concat('law-yamashita-app.js'))
		.pipe($.plumber({
		errorHandler: $.notify.onError('Error: <%= error.message %>')
	}))
		.pipe($.uglify())
		.pipe($.rename({
		extname: '.min.js'
	}))
		.pipe(gulp.dest( path.js ))
		.pipe(browserSync.reload({ stream: true }));
});

// Browser Sync
gulp.task('server', function() {
	browserSync({
		proxy: 'www.law-yamashita.dev/'
	});
});
gulp.task('bs-reload', function() {
	browserSync.reload();
});
/* =========================================  WATCH  ================================ */
gulp.task('watch', [ 'style', 'precom-scripts', 'src-js', 'server' ], function() {
	gulp.watch( path.sass + '{,/**/}{,/**/}{,/**/}{,/**/}*.scss', ['style'] );
	gulp.watch( path.precom + '*.js', ['precom-scripts'] );
	gulp.watch( path.src + '*.js', ['src-js'] );
	gulp.watch( './{,/**/}{,/**/}{,/**/}{,/**/}*.html', ['bs-reload'] );
});
gulp.task('default', ['watch']);
