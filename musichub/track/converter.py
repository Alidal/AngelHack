import os
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


def duration(note):
    duration = note.beat.duration.value
    if duration > 8:
        return "1/%i" % (duration / 8)
    return str(1 / (duration / 8))


def add_effects(note, effects):
    if effects.staccato:
        note = '.' + note
    # if effects.acce
    return note


def convert(track):
    file_path = os.path.join(track.repository.split('.')[0], track.title)
    song = guitarpro.parse(file_path)

    tracks = {}
    # All tracks
    for track in song.tracks:
        headers = generate_header(track.song)
        measures = [headers, ]
        # Every measure
        for measure in track.measures:
            cur_measure = ""
            # Every beat
            for beat in measure.voices[0].beats:
                cur_beat = "["
                # Every note in chord (if it is chord)
                for note in beat.notes:
                    abc_note = get_abc_note_from_midi(note.realValue)
                    abc_note += duration(note)
                    abc_note = add_effects(abc_note, note.effect)
                    cur_beat += abc_note
                cur_beat += "] "
                cur_measure += cur_beat
                if len(measures) % 4 == 0:
                    cur_measure += "\n"
            measures.append(cur_measure)
        measures[-1] += " |]"
        measures[1] = "[" + measures[1]
        tracks[track.name] = "| ".join(measures)
    return tracks
