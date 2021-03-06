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
        redirect_url = '/' + user
        formData = new FormData
        formData.append $('input:text').attr("id"), $('input:text').val()
        formData.append "file", document.getElementById('id_file').files[0]
        if document.getElementById('id_repo_pk')
            formData.append "pk", document.getElementById('id_repo_pk').value
            redirect_url += '/' + document.getElementById('id_repo_pk').value

        $.ajax
            method: "POST",
            url: "/upload",
            dataType: "json",
            processData: false,
            contentType: false,
            data: formData
        .success (data)->
            if data.success
                window.location.replace redirect_url