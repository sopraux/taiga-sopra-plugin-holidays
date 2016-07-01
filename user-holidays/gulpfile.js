var gulp = require('gulp');
var $ = require('gulp-load-plugins')();
var merge = require('merge-stream');

var paths = {
    jade: 'partials/*.jade',
    styles: [
        'bower_components/jquery-ui/themes/smoothness/jquery-ui.min.css',
        'styles/*.scss'
    ],
    coffee: 'coffee/*.coffee',
    vendor: [
        'bower_components/jquery-ui/jquery-ui.min.js',
        'bower_components/jqui-multi-dates-picker/jquery-ui.multidatespicker.js'
    ],
    images: 'bower_components/jquery-ui/themes/base/images/*',
    dist: 'dist/'
};

gulp.task('copy-config', function() {
    return gulp.src('user-holidays.json')
        .pipe(gulp.dest(paths.dist));
});

gulp.task('compile', function() {
    var jade = gulp.src(paths.jade)
        .pipe($.plumber())
        .pipe($.cached('jade'))
        .pipe($.jade({pretty: true}))
        .pipe($.angularTemplatecache({
            transformUrl: function(url) {
                return '/plugins/user-holidays/' + url;
            }
        }))
        .pipe($.remember('jade'));

    var coffee = gulp.src(paths.coffee)
        .pipe($.plumber())
        .pipe($.cached('coffee'))
        .pipe($.coffee())
        .pipe($.remember('coffee'));

    var vendor = gulp.src(paths.vendor)
        .pipe($.remember('vendor'));

    return merge(jade, coffee, vendor)
        .pipe($.concat('holidays.js'))
        //.pipe($.uglify({mangle:false, preserveComments: false}))
        .pipe(gulp.dest(paths.dist));
});

gulp.task('compile-styles', function() {
    return gulp.src(paths.styles)
        .pipe($.sass({outputStyle: 'compressed'}).on('error', $.sass.logError))
        .pipe($.concat('holidays.css'))
        .pipe(gulp.dest(paths.dist));
});

gulp.task('copy-images', function() {
    return gulp.src(paths.images)
        .pipe(gulp.dest(paths.dist+'/images'));
});

gulp.task('watch', function() {
    gulp.watch([paths.jade, paths.coffee, paths.styles], ['compile', 'compile-styles']);
});

gulp.task('default', ['copy-config', 'compile', 'compile-styles', 'copy-images', 'watch']);

gulp.task('build', ['copy-config', 'compile', 'compile-styles', 'copy-images']);
