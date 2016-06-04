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
        document.getElementById('id_file').files = files

    obj.on 'click', (e)->
        e.preventDefault()
        $('#id_file').click()

    $('#id_file').on 'change', (e)->
        obj.removeClass('hover').addClass('drop').html('<i class="fa fa-cloud-upload" aria-hidden="true"></i> File successfuly uploaded')
       
    $('form').submit (e)->
        e.preventDefault()
        formData = new FormData
        formData.append "input", $('input:text').val()
        formData.append "file", document.getElementById('id_file').files[0]

        $.ajax
            method: "POST",
            url: "/upload",
            dataType: "json",
            processData: false,
            contentType: false,
            data: formData
        .success (data)->
            console.log data