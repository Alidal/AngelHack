import guitarpro


def generate_header(song):
    song_text = [line.lyrics for line in song.lyrics.lines]

    if any(song_text):
        # Delete all empty strings
        song_text = filter(None, song_text)
        song_text = "\nW: ".join(song_text)
        song_text = song_text.replace('\r\n', '\nW:')
    else:
        song_text = ""

    meta = "X: 1\n"
    meta += "T: %s - %s\n" % (song.artist, song.title)  # Title
    meta += "C: %s\n" % song.music  # Composer
    key = song.key.name.replace("Major", "")
    meta += "K: %s\n" % key  # Tonality
    meta += "M: %s\n" % "C"  # TODO: Replace.
    meta += "Q: %d\n" % song.tempo  # Tempo
    meta += "W: %s\n" % song_text  # Song words
    return meta


def get_abc_note_from_midi(code):
    table = {
        0: 'C',
        1: '^C',
        2: 'D',
        3: '^D',
        4: 'E',
        5: 'F',
        6: '^F',
        7: 'G',
        8: '^G',
        9: 'A',
        10: '^A',
        11: 'B',
    }

    note = table[code % 12]
    octave = int((code - 60) / 12)
    if octave < 0:
        note += "".join(',' * (-octave))
    elif octave > 0:
        note += "".join('\'' * octave)
    return note


def duration(beat):
    duration = 8 / beat.duration.value
    if beat.duration.isDotted:
        duration += 0.5
    if duration < 1.0:
        return "1/%i" % int(1 / duration)
    return str(int(duration))


def add_effects(note, effects):
    if effects.accentuatedNote:
        note = "L" + note
    if effects.heavyAccentuatedNote:
        note = "LL" + note
    if effects.staccato:
        note = "." + note

    return note


def convert(file=None):
    """
    Convert Guitar Pro files to ABC notation.
    Takes GP* file instance as argument.
    Returns dict with tracks as kays, and ABC notation as values.
    """
    song = guitarpro.parse(file)

    tracks = {}
    # All tracks
    for track in song.tracks:
        headers = generate_header(track.song)
        measures = [headers, ]
        # Every measure
        for measure in track.measures:
            cur_measure = ""
            # Hack for connecting notes
            previous_duration = 0

            # Every beat
            for i, beat in enumerate(measure.voices[0].beats):
                cur_beat = "["
                # Every note in chord (if it is chord)
                if not beat.notes:
                    # Handle pauses
                    cur_beat = "z%s " % duration(beat)
                else:
                    # Handle notes
                    for note in beat.notes:
                        abc_note = get_abc_note_from_midi(note.realValue)
                        abc_note += duration(beat)
                        abc_note = add_effects(abc_note, note.effect)
                        cur_beat += abc_note
                    cur_beat += "]"
                    # Hackaton
                    if i != 0 and (i % 2 == 0 or beat.duration.value != previous_duration):
                        cur_beat += " "
                        previous_duration = beat.duration.value
                cur_measure += cur_beat
                cur_measure = cur_measure.replace("\n", "")
                if len(measures) % 4 == 0:
                    cur_measure += "\n"
            measures.append(cur_measure)
        measures[-1] += " |]"
        tracks[track.name] = "| ".join(measures)
    return tracks
