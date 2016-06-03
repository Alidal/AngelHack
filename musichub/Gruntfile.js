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
          'static/build/js/formUtil.js': ['static/dev/coffee/formUtil.coffee'],
        }
      }
    },
    concat: {
      libs: {
        files: {
          'static/build/css/libs.css': ['node_modules/bootstrap/dist/css/bootstrap.min.css'],
          'static/build/js/libs.js': [
            'node_modules/jquery/dist/jquery.min.js'
          ]
        }
      }
    },
    copy: {
      fonts: {
        files: [
          {expand: true, flatten: true, src: 'node_modules/bootstrap/dist/fonts/**', dest: 'static/build/fonts/'}
        ]
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-coffee');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-copy');

  grunt.registerTask('default', ['coffee', 'less', 'concat', 'copy']);
};