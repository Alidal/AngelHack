$ ->
    tunebookString = $('#notesABC').text()
    window.tunebook = new ABCJS.TuneBook tunebookString
    window.tuneObjectArray = ABCJS.renderAbc "sheetABC", tunebookString
    window.tuneObjectArrayMIDI = ABCJS.renderMidi "midi", tunebookString
    $('.edit').after('<a href="' + $('#midi a').attr('href') + '" download="' + $('.song-title').html() + '.mid" class="btn btn-success"><i class="fa fa-cloud-download" aria-hidden="true"></i> Download MIDI</a>')