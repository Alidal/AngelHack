window.ViewBind = ()->
    $('#sheetABC rect').bind 'click', ()->
        textArea = $('#textarea')
        len = textArea.val().length;
        start = textArea[0].selectionStart
        end = textArea[0].selectionEnd
        selectedText = textArea.val().substring start, end
        window.mainSelected = text: selectedText, start: start, end: end, len: len
        $('#chord').val(selectedText)
        $('#changer').addClass('active')

window.mainSelected = {}

$ ->
    window.abc_editor = new ABCJS.Editor "textarea", paper_id: "sheetABC"
    window.abc_editor.paramChanged add_classes: true, listener: highlight: window.ViewBind, modelChanged: ()->
        ViewBind()
    ViewBind()

    $('#save').on 'click', (e)->
        e.preventDefault()
        replacement = $('#chord').val()
        $('#textarea').val($('#textarea').val().substring(0, mainSelected.start) + replacement + $('#textarea').val().substring(mainSelected.end, mainSelected.len));
        $('#textarea').trigger 'change'
        $('#changer').removeClass('active')


    $('form').submit (e)->
        e.preventDefault()
        formData = new FormData
        formData.append "description", document.getElementById('id_commitdescription').value
        formData.append "notes", document.getElementById('textarea').value
        formData.append "data", data

        $.ajax
            method: "POST",
            url: "/track/save",
            dataType: "json",
            processData: false,
            contentType: false,
            data: formData
        .success (data)->
            if data.success
                window.location.refresh()


    