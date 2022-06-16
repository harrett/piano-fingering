import music21 as m21
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

class Note:
    @staticmethod
    def to_note_num(note: m21.note.Note) -> int:
        """music21のNoteオブジェクトからmidiノートナンバーを返す"""
        octave = note.octave
        if '-' in note.name:
            pitch = ['C', 'D-', 'D', 'E-', 'E', 'F', 'G-', 'G', 'A-', \
                'A', 'B-', 'B'].index(note.name)
        else:
            pitch = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', \
                'A', 'A#', 'B'].index(note.name)

        return 12 + 12*octave + pitch

    def __init__(self, note: m21.note.Note, time: float):
        """ノートナンバー, 黒鍵, timeを初期化"""
        self.note_num = self.to_note_num(note)
        self.black = ('-' in note.name) or ('#' in note.name)
        self.time = time


def midi2notes(path):
    song = m21.converter.parse(path)
    song.plot()
    plt.savefig('static/tmp/tmp.png')
    notes = []

    for part in song[:2]: # 全トラック
        track_notes = []
        time = 0
        for measure in part: # 全小節
            for chord in measure.notes: # 全ノート(コード)
                chord_notes = chord.pitches # ノートに分解
                # 一番高い音のインデックスを取得
                idx = np.array(
                    [Note.to_note_num(note) for note in chord_notes]).argmax()
                note = Note(chord_notes[int(idx)], time)
                track_notes.append(note)
                time += chord.quarterLength # 時間を更新
        notes.append(track_notes)

    return notes