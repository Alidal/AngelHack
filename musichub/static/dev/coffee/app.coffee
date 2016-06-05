$ ->
    dfd = $.Deferred();

    $(window).on('load', dfd.resolve);

    setTimeout dfd.resolve, 5 * 1000

    dfd.done ()-> $('#loading').hide(500)
