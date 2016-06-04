$ ->
    tunebookStringOld = $('#notesABCOld').text()
    window.tunebookOld = new ABCJS.TuneBook tunebookStringOld
    window.tuneObjectArrayOld = ABCJS.renderAbc "sheetABCOld", tunebookStringOld, undefined, staffwidth: 500, scale: 0.8, add_classes: true
    window.tuneObjectArrayMIDIOld = ABCJS.renderMidi "midi", tunebookStringOld
    $('#notesOld').prepend('<a href="' + $('#midiOld a').attr('href') + '" download="' + $('.song-title').html() + '.mid" class="btn btn-warning pull-left"><i class="fa fa-cloud-download" aria-hidden="true"></i> Download Old MIDI</a>')


    tunebookStringNew = $('#notesABCNew').text()
    window.tunebookNew = new ABCJS.TuneBook tunebookStringNew
    window.tuneObjectArrayNew = ABCJS.renderAbc "sheetABCNew", tunebookStringNew, undefined, staffwidth: 500, scale: 0.8, add_classes: true
    window.tuneObjectArrayMIDINew = ABCJS.renderMidi "midi", tunebookStringNew
    $('#notesNew').prepend('<a href="' + $('#midiNew a').attr('href') + '" download="' + $('.song-title').html() + '.mid" class="btn btn-success pull-right"><i class="fa fa-cloud-download" aria-hidden="true"></i> Download New MIDI</a>')

    changes.map (el)->
    	l = '.l' + Math.floor(el / 4)
    	m = '.m' + (el % 4 - 1)
    	$('#notesOld ' + l + m).map (i, el)->
    		$(el).attr('fill', 'red')
    	$('#notesNew ' + l + m).map (i, el)->
    		$(el).attr('fill', 'green')