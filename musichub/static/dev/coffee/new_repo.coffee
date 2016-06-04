$ ->
    obj = $("#drop")

    obj.on 'dragenter', (e)->
        e.stopPropagation();
        e.preventDefault();
        $(this).text('YEAAAAAAAAAH').addClass 'hover'

    obj.on 'dragover', (e)->
        e.stopPropagation();
        e.preventDefault();
        $(this).html('<i class="fa fa-cloud-upload" aria-hidden="true"></i> drop files here').removeClass 'hover'

    obj.on 'drop', (e)->
        $(this).removeClass('hover').addClass('drop').html('<i class="fa fa-cloud-upload" aria-hidden="true"></i> File successfuly uploaded')
        e.preventDefault();
        files = e.originalEvent.dataTransfer.files
        document.getElementById('fileinput').files = files

    obj.on 'click', (e)->
        e.preventDefault();
        $('#fileinput').click()

    $('#fileinput').on 'change', (e)->
        obj.removeClass('hover').addClass('drop').html('<i class="fa fa-cloud-upload" aria-hidden="true"></i> File successfuly uploaded')
       