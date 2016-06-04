tunebookString = $('#notesABC').text()
window.tuneObjectArray = ABCJS.renderAbc "sheetABC", tunebookString
$('svg path').map (i, el)-> $(el).attr fill: '#FFFFFF'