module.exports = function(grunt) {
  grunt.initConfig({
    watch: {
      scripts: {
        files: ['static/dev/coffee/**/*.coffee'],
        tasks: ['coffee:static']
      },
      styles: {
        files: ['static/dev/less/**/*.less'],
        tasks: ['less:dev']
      },
      jsx: {
        files: ['static/dev/templates/**/*.jsx'],
        tasks: ['react']
      }
    },
    less: {
      dev: {
        options : {
          compress: false
        },
        files: {
          'static/build/css/style.css': ['static/dev/less/**/*.less']
        }
      }
    },
    coffee: {
      static: {
        options: {
          join: true
        },
        files: {
          'static/build/js/repo.js': ['static/dev/coffee/repo.coffee'],
          'static/build/js/home.js': ['static/dev/coffee/home.coffee'],
          'static/build/js/profile.js': ['static/dev/coffee/profile.coffee'],
        }
      }
    },
    concat: {
      libs: {
        files: {
          'static/build/css/libs.css': [
            'node_modules/bootstrap/dist/css/bootstrap.min.css',
            'node_modules/font-awesome/css/font-awesome.min.css'
          ],
          'static/build/js/libs.js': [
            'node_modules/jquery/dist/jquery.min.js',
            'static/dev/js/**/*.js',
            'node_modules/bootstrap/dist/js/bootstrap.min.js',
          ]
        }
      }
    },
    copy: {
      fonts: {
        files: [
          {expand: true, flatten: true, src: 'node_modules/bootstrap/dist/fonts/**', dest: 'static/build/fonts/'},
          {expand: true, flatten: true, src: 'node_modules/font-awesome/fonts/**', dest: 'static/build/fonts/'}
        ]
      }
    },
  });

  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-coffee');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-copy');

  grunt.registerTask('default', ['coffee', 'less', 'concat', 'copy']);
};