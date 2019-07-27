import pretty_midi
import cozmo
from cozmo.util import degrees

# COZMO_MAX_SING = 255
COZMO_MAX_SING = 69

# cozmoとMIDIデータの比較表
note_pitch_array = {
    24 : cozmo.song.NoteTypes.C2,
    25 : cozmo.song.NoteTypes.C2_Sharp,
    26 : cozmo.song.NoteTypes.D2,
    27 : cozmo.song.NoteTypes.D2_Sharp,
    28 : cozmo.song.NoteTypes.E2,
    29 : cozmo.song.NoteTypes.F2,
    30 : cozmo.song.NoteTypes.F2_Sharp,
    31 : cozmo.song.NoteTypes.G2,
    32 : cozmo.song.NoteTypes.G2_Sharp,
    33 : cozmo.song.NoteTypes.A2,
    34 : cozmo.song.NoteTypes.A2_Sharp,
    35 : cozmo.song.NoteTypes.B2,

    # cozmoの音階
    36 : cozmo.song.NoteTypes.C2,
    37 : cozmo.song.NoteTypes.C2_Sharp,
    38 : cozmo.song.NoteTypes.D2,
    39 : cozmo.song.NoteTypes.D2_Sharp,
    40 : cozmo.song.NoteTypes.E2,
    41 : cozmo.song.NoteTypes.F2,
    42 : cozmo.song.NoteTypes.F2_Sharp,
    43 : cozmo.song.NoteTypes.G2,
    44 : cozmo.song.NoteTypes.G2_Sharp,
    45 : cozmo.song.NoteTypes.A2,
    46 : cozmo.song.NoteTypes.A2_Sharp,
    47 : cozmo.song.NoteTypes.B2,
    48 : cozmo.song.NoteTypes.C3,
    49 : cozmo.song.NoteTypes.C3_Sharp,

    # その他音階    
    # 48 : cozmo.song.NoteTypes.C2,
    # 49 : cozmo.song.NoteTypes.C2_Sharp,
    50 : cozmo.song.NoteTypes.D2,
    51 : cozmo.song.NoteTypes.D2_Sharp,
    52 : cozmo.song.NoteTypes.E2,
    53 : cozmo.song.NoteTypes.F2,
    54 : cozmo.song.NoteTypes.F2_Sharp,
    55 : cozmo.song.NoteTypes.G2,
    56 : cozmo.song.NoteTypes.G2_Sharp,
    57 : cozmo.song.NoteTypes.A2,
    58 : cozmo.song.NoteTypes.A2_Sharp,
    59 : cozmo.song.NoteTypes.B2,

    60 : cozmo.song.NoteTypes.C2,
    61 : cozmo.song.NoteTypes.C2_Sharp,
    62 : cozmo.song.NoteTypes.D2,
    63 : cozmo.song.NoteTypes.D2_Sharp,
    64 : cozmo.song.NoteTypes.E2,
    65 : cozmo.song.NoteTypes.F2,
    66 : cozmo.song.NoteTypes.F2_Sharp,
    67 : cozmo.song.NoteTypes.G2,
    68 : cozmo.song.NoteTypes.G2_Sharp,
    69 : cozmo.song.NoteTypes.A2,
    70 : cozmo.song.NoteTypes.A2_Sharp,
    71 : cozmo.song.NoteTypes.B2,

    72 : cozmo.song.NoteTypes.C2,
    73 : cozmo.song.NoteTypes.C2_Sharp,
    74 : cozmo.song.NoteTypes.D2,
    75 : cozmo.song.NoteTypes.D2_Sharp,
    76 : cozmo.song.NoteTypes.E2,
    77 : cozmo.song.NoteTypes.F2,
    78 : cozmo.song.NoteTypes.F2_Sharp,
    79 : cozmo.song.NoteTypes.G2,
    80 : cozmo.song.NoteTypes.G2_Sharp,
    81 : cozmo.song.NoteTypes.A2,
    82 : cozmo.song.NoteTypes.A2_Sharp,
    83 : cozmo.song.NoteTypes.B2,

    84 : cozmo.song.NoteTypes.C2,
    85 : cozmo.song.NoteTypes.C2_Sharp,
    86 : cozmo.song.NoteTypes.D2,
    87 : cozmo.song.NoteTypes.D2_Sharp,
    88 : cozmo.song.NoteTypes.E2,
    89 : cozmo.song.NoteTypes.F2,
    90 : cozmo.song.NoteTypes.F2_Sharp,
    91 : cozmo.song.NoteTypes.G2,
    92 : cozmo.song.NoteTypes.G2_Sharp,
    93 : cozmo.song.NoteTypes.A2,
    94 : cozmo.song.NoteTypes.A2_Sharp,
    95 : cozmo.song.NoteTypes.B2,
}
set_note_datas = []


# MIDIデータを取り込む
def load_midi():
    midi_data = pretty_midi.PrettyMIDI('midi/midi_data/Pokemon - pokecentre theme.mid')
    # midi_data = pretty_midi.PrettyMIDI('midi/midi_data/Pokemon RedBlueYellow - Pokemon Tower.mid')
    note_count = 0;

    for note in midi_data.instruments[0].notes:
        set_note_data = {}
        if note_count >= COZMO_MAX_SING:
            break

        # print(note.pitch)
        set_note_data['note']=note_pitch_array[note.pitch]

        print(note.end - note.start)
        duration = round((note.end - note.start), 1)
        select_duration = ''
        if duration == 0.2:
            # print('Quarter')
            select_duration = cozmo.song.NoteDurations.Quarter
        elif duration == 0.4:
            # print('Half')
            select_duration = cozmo.song.NoteDurations.Half
        elif duration < 1.0:
            # print('ThreeQuarter')
            select_duration = cozmo.song.NoteDurations.ThreeQuarter
        else:
            # print('Whole')
            select_duration = cozmo.song.NoteDurations.Whole

        set_note_data['duration']=select_duration
        set_note_datas.append(set_note_data)
        note_count+=1
        
    # print(set_note_datas)


# cozmoに歌わせる関数
def cozmo_sing(robot: cozmo.robot.Robot):
    sing_notes = []
    for note in set_note_datas:

        sing_notes.append(cozmo.song.SongNote(note.get('note'), note.get('duration')))
        # sing_notes.append(cozmo.song.SongNote(note.get('note')))

    # sing_notes = [
    #     cozmo.song.SongNote(cozmo.song.NoteTypes.D2, cozmo.song.NoteDurations.Quarter),
    #     cozmo.song.SongNote(cozmo.song.NoteTypes.C2, cozmo.song.NoteDurations.Half),
    #     cozmo.song.SongNote(cozmo.song.NoteTypes.E2, cozmo.song.NoteDurations.ThreeQuarter),
    #     cozmo.song.SongNote(cozmo.song.NoteTypes.F2, cozmo.song.NoteDurations.Whole),
    # ]

    # robot.play_anim_trigger(cozmo.anim.Triggers.Singing_GetIn).wait_for_completed()

    robot.play_song(sing_notes, loop_count=1, in_parallel=True).wait_for_completed()

    # robot.play_anim_trigger(cozmo.anim.Triggers.SoftSparkUpgradeTracks, loop_count=3, in_parallel=True).wait_for_completed()

    # robot.play_anim_trigger(cozmo.anim.Triggers.LookInPlaceForFacesHeadMovePause, loop_count=3, in_parallel=True).wait_for_completed()

    # robot.play_anim_trigger(cozmo.anim.Triggers.Singing_GetOut).wait_for_completed()
    


# midi読み込む
load_midi()

# cozmo歌って
cozmo.run_program(cozmo_sing)