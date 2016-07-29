var gulp        = require('gulp'),
	$           = require('gulp-load-plugins')(),
	browserSync = require('browser-sync');


// Browser Sync
gulp.task('server', function() {
	browserSync({
		server: {
			baseDir: './',
			routes: {
				'/node_modules': 'node_modules'
			}
		},
		notify: true
	});
});
gulp.task('bs-reload', function() {
	browserSync.reload();
});
/* =========================================  WATCH  ================================ */
gulp.task('watch', [ 'server' ], function() {
	gulp.watch( './{,/**/}{,/**/}{,/**/}{,/**/}*.html', ['bs-reload'] );
});
gulp.task('default', ['watch']);
