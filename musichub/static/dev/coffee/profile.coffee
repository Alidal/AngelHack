$ ->
    $('.follow').click (e)->
        e.preventDefault()
        if $(this).hasClass('btn-success')
            $(this).removeClass('btn-success').addClass('btn-default').html '<i class="fa fa-users" aria-hidden="true"></i> Unfollow'
        else
            $(this).removeClass('btn-default').addClass('btn-success').html '<i class="fa fa-users" aria-hidden="true"></i> Follow'