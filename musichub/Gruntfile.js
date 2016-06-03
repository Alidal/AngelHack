module.exports = function(grunt) {
  grunt.initConfig({
    watch: {
      scripts: {
        files: ['static/src/coffee/**/*.coffee'],
        tasks: ['coffee:static']
      },
      styles: {
        files: ['static/src/less/**/*.less'],
        tasks: ['less:dev']
      }
    },
    less: {
      dev: {
        options : {
          compress: true
        },
        files: {
          'static/build/css/style.css': ['static/src/less/**/*.less']
        }
      }
    },
    coffee: {
      static: {
        options: {
          join: true
        },
        files: {
          'static/build/js/formUtil.js': ['static/src/coffee/formUtil.coffee'],
        }
      }
    },
    concat: {
      libs: {
        files: {
          'static/build/css/libs.css': ['node_modules/bootstrap/dist/css/bootstrap.min.css']
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