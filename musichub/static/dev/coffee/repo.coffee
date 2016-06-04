$ ->
    tunebookString = $('#notesABC').text()
    window.tunebook = new ABCJS.TuneBook tunebookString
    console.log tunebook.tunes[0]
    window.tuneObjectArray = ABCJS.renderAbc "sheetABC", tunebookString
    window.tuneObjectArrayMIDI = ABCJS.renderMidi "midi", tunebookString