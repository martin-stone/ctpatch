
import difflib
from pprint import pformat
from ctpatch import (DistortionType, Envelope, Filter, FilterType, Footer, Fx, Header, Lfo, LfoFadeMode,
                     LfoFlags, LfoWaveform, MacroKnob, MacroKnobDestination, MacroKnobRange, Mixer,
                     ModMatrix, ModMatrixDestination, ModMatrixSource, Osc, OscWaveform, Meta, PatchSysex,
                     PolyphonyMode, ReplaceCurrentPatchCommand, Voice, read_syx, write_syx)


test_patch = PatchSysex(
    header=Header(sysex=0,
                  mfr_id=b'\x00 )',
                  prod_type=1,
                  prod_num=100),
    command=ReplaceCurrentPatchCommand(command_id=0,
                                       location=4,
                                       _reserved=5),
    meta=Meta(_name=b'Initial Patch   ',
              category=6,
              genre=7,
              _reserved=b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f'),
    voice=Voice(polyphony_mode=PolyphonyMode.MONO,
                portamento_rate=8,
                pre_glide=9,
                keyboard_octave=10),
    oscillators=[Osc(wave=OscWaveform.ANALOGUE_PULSE,
                     wave_interpolate=11,
                     pulse_width_index=12,
                     virtual_sync_depth=13,
                     density=14,
                     density_detune=15,
                     semitones=16,
                     cents=17,
                     pitch_bend=18),
                 Osc(wave=OscWaveform.DIGITAL_NASTY_1,
                     wave_interpolate=19,
                     pulse_width_index=20,
                     virtual_sync_depth=21,
                     density=22,
                     density_detune=23,
                     semitones=24,
                     cents=25,
                     pitch_bend=26)],

    mixer=Mixer(osc1_level=27,
                osc2_level=28,
                ring_mod_level12=29,
                noise_level=30,
                pre_fx_level=31,
                post_fx_level=32),
    filter=Filter(routing=33,
                  drive=34,
                  drive_type=DistortionType.DIODE,
                  type=FilterType.BAND_PASS_12DB,
                  frequency=35,
                  track=36,
                  resonance=37,
                  q_normalise=38,
                  env2_to_freq=39),
    envelopes=[Envelope(velocity_or_delay=40,
                        attack=41,
                        decay=42,
                        sustain=43,
                        release=44),
               Envelope(velocity_or_delay=45,
                        attack=46,
                        decay=47,
                        sustain=48,
                        release=49),
               Envelope(velocity_or_delay=50,
                        attack=51,
                        decay=52,
                        sustain=53,
                        release=54)],
    lfos=[Lfo(waveform=LfoWaveform.MINOR_7,
              phase_offset=55,
              slew_rate=56,
              delay=57,
              delay_sync=58,
              rate=59,
              rate_sync=60,
              flags=LfoFlags(True, False, True, False, LfoFadeMode.FADE_OUT)),
          Lfo(waveform=LfoWaveform.MAJOR_7,
              phase_offset=61,
              slew_rate=62,
              delay=63,
              delay_sync=64,
              rate=65,
              rate_sync=66,
              flags=LfoFlags(False, True, False, True, LfoFadeMode.GATE_IN))],
    fx=Fx(distortion_level=67,
          _fx_reserved1=68,
          chorus_level=69,
          _fx_reserved2=70,
          _fx_reserved3=71,
          equaliser_bass_frequency=72,
          equaliser_bass_level=73,
          equaliser_mid_frequency=74,
          equaliser_mid_level=75,
          equaliser_treble_frequency=76,
          equaliser_treble_level=77,
          _fx_reserved45678=b'\x01\x00\x00\x00\x0f',
          distortion_type=DistortionType.VALVE,
          distortion_compensation=78,
          chorus_type=79,
          chorus_rate=80,
          chorus_rate_sync=81,
          chorus_feedback=82,
          chorus_mod_depth=83,
          chorus_delay=84),
    mod_matrix=[ModMatrix(source1=ModMatrixSource.DIRECT,
                          source2=ModMatrixSource.VELOCITY,
                          depth=85,
                          destination=ModMatrixDestination.OSC_1_AND_2_PITCH),
                ModMatrix(source1=ModMatrixSource.KEYBOARD,
                          source2=ModMatrixSource.LFO_1_PLUS,
                          depth=86,
                          destination=ModMatrixDestination.OSC_1_PITCH),
                ModMatrix(source1=ModMatrixSource.LFO_1_PLUS_MINUS,
                          source2=ModMatrixSource.LFO_2_PLUS,
                          depth=87,
                          destination=ModMatrixDestination.OSC_2_PITCH),
                ModMatrix(source1=ModMatrixSource.LFO_2_PLUS_MINUS,
                          source2=ModMatrixSource.ENV_AMP,
                          depth=88,
                          destination=ModMatrixDestination.OSC_1_V_SYNC),
                ModMatrix(source1=ModMatrixSource.ENV_FILTER,
                          source2=ModMatrixSource.DIRECT,
                          depth=89,
                          destination=ModMatrixDestination.OSC_2_V_SYNC),
                ModMatrix(source1=ModMatrixSource.VELOCITY,
                          source2=ModMatrixSource.KEYBOARD,
                          depth=90,
                          destination=ModMatrixDestination.OSC_1_PULSE_WIDTH_INDEX),
                ModMatrix(source1=ModMatrixSource.LFO_1_PLUS,
                          source2=ModMatrixSource.LFO_1_PLUS_MINUS,
                          depth=91,
                          destination=ModMatrixDestination.OSC_2_PULSE_WIDTH_INDEX),
                ModMatrix(source1=ModMatrixSource.LFO_2_PLUS,
                          source2=ModMatrixSource.LFO_2_PLUS_MINUS,
                          depth=92,
                          destination=ModMatrixDestination.OSC_1_LEVEL),
                ModMatrix(source1=ModMatrixSource.ENV_AMP,
                          source2=ModMatrixSource.ENV_FILTER,
                          depth=93,
                          destination=ModMatrixDestination.OSC_2_LEVEL),
                ModMatrix(source1=ModMatrixSource.DIRECT,
                          source2=ModMatrixSource.VELOCITY,
                          depth=94,
                          destination=ModMatrixDestination.NOISE_LEVEL),
                ModMatrix(source1=ModMatrixSource.KEYBOARD,
                          source2=ModMatrixSource.LFO_1_PLUS,
                          depth=95,
                          destination=ModMatrixDestination.RING_MODULATION_LEVEL),
                ModMatrix(source1=ModMatrixSource.LFO_1_PLUS_MINUS,
                          source2=ModMatrixSource.LFO_2_PLUS,
                          depth=96,
                          destination=ModMatrixDestination.FILTER_DRIVE_AMOUNT),
                ModMatrix(source1=ModMatrixSource.LFO_2_PLUS_MINUS,
                          source2=ModMatrixSource.ENV_AMP,
                          depth=97,
                          destination=ModMatrixDestination.FILTER_FREQUENCY),
                ModMatrix(source1=ModMatrixSource.ENV_FILTER,
                          source2=ModMatrixSource.DIRECT,
                          depth=98,
                          destination=ModMatrixDestination.FILTER_RESONANCE),
                ModMatrix(source1=ModMatrixSource.VELOCITY,
                          source2=ModMatrixSource.KEYBOARD,
                          depth=99,
                          destination=ModMatrixDestination.LFO_1_RATE),
                ModMatrix(source1=ModMatrixSource.LFO_1_PLUS,
                          source2=ModMatrixSource.LFO_1_PLUS_MINUS,
                          depth=100,
                          destination=ModMatrixDestination.LFO_2_RATE),
                ModMatrix(source1=ModMatrixSource.LFO_2_PLUS,
                          source2=ModMatrixSource.LFO_2_PLUS_MINUS,
                          depth=101,
                          destination=ModMatrixDestination.AMP_ENVELOPE_DECAY),
                ModMatrix(source1=ModMatrixSource.ENV_AMP,
                          source2=ModMatrixSource.ENV_FILTER,
                          depth=102,
                          destination=ModMatrixDestination.FILTER_ENVELOPE_DECAY),
                ModMatrix(source1=ModMatrixSource.DIRECT,
                          source2=ModMatrixSource.VELOCITY,
                          depth=103,
                          destination=ModMatrixDestination.OSC_1_AND_2_PITCH),
                ModMatrix(source1=ModMatrixSource.KEYBOARD,
                          source2=ModMatrixSource.LFO_1_PLUS,
                          depth=104,
                          destination=ModMatrixDestination.OSC_1_PITCH)],
    macro_knobs=[MacroKnob(position=105,
                           ranges=[MacroKnobRange(destination=MacroKnobDestination.NO_DESTINATION,
                                                  start_pos=106,
                                                  end_pos=107,
                                                  depth=108),
                                   MacroKnobRange(destination=MacroKnobDestination.PORTAMENTO_RATE,
                                                  start_pos=109,
                                                  end_pos=110,
                                                  depth=111),
                                   MacroKnobRange(destination=MacroKnobDestination.POST_FX_VOLUME,
                                                  start_pos=112,
                                                  end_pos=113,
                                                  depth=114),
                                   MacroKnobRange(destination=MacroKnobDestination.O1_WAVE_INTERPOLATE,
                                                  start_pos=115,
                                                  end_pos=116,
                                                  depth=117)]),
                 MacroKnob(position=118,
                           ranges=[MacroKnobRange(destination=MacroKnobDestination.O1_PULSE_WIDTH_INDEX,
                                                  start_pos=119,
                                                  end_pos=120,
                                                  depth=121),
                                   MacroKnobRange(destination=MacroKnobDestination.O1_VSYNC_DEPTH,
                                                  start_pos=122,
                                                  end_pos=123,
                                                  depth=124),
                                   MacroKnobRange(destination=MacroKnobDestination.O1_DENSITY,
                                                  start_pos=125,
                                                  end_pos=126,
                                                  depth=0),
                                   MacroKnobRange(destination=MacroKnobDestination.O1_DENSITY_DETUNE,
                                                  start_pos=1,
                                                  end_pos=2,
                                                  depth=3)]),
                 MacroKnob(position=4,
                           ranges=[MacroKnobRange(destination=MacroKnobDestination.O1_SEMITONES_TUNE,
                                                  start_pos=5,
                                                  end_pos=6,
                                                  depth=7),
                                   MacroKnobRange(destination=MacroKnobDestination.O1_CENTS_TUNE,
                                                  start_pos=8,
                                                  end_pos=9,
                                                  depth=10),
                                   MacroKnobRange(destination=MacroKnobDestination.O2_WAVE_INTERPOLATE,
                                                  start_pos=11,
                                                  end_pos=12,
                                                  depth=13),
                                   MacroKnobRange(destination=MacroKnobDestination.O2_PULSE_WIDTH_INDEX,
                                                  start_pos=14,
                                                  end_pos=15,
                                                  depth=16)]),
                 MacroKnob(position=17,
                           ranges=[MacroKnobRange(destination=MacroKnobDestination.O2_VSYNC_DEPTH,
                                                  start_pos=18,
                                                  end_pos=19,
                                                  depth=20),
                                   MacroKnobRange(destination=MacroKnobDestination.O2_DENSITY,
                                                  start_pos=21,
                                                  end_pos=22,
                                                  depth=23),
                                   MacroKnobRange(destination=MacroKnobDestination.O2_DENSITY_DETUNE,
                                                  start_pos=24,
                                                  end_pos=25,
                                                  depth=26),
                                   MacroKnobRange(destination=MacroKnobDestination.O2_SEMITONES_TUNE,
                                                  start_pos=27,
                                                  end_pos=28,
                                                  depth=29)]),
                 MacroKnob(position=30,
                           ranges=[MacroKnobRange(destination=MacroKnobDestination.O2_CENTS_TUNE,
                                                  start_pos=31,
                                                  end_pos=32,
                                                  depth=33),
                                   MacroKnobRange(destination=MacroKnobDestination.OSC1_VOLUME,
                                                  start_pos=34,
                                                  end_pos=35,
                                                  depth=36),
                                   MacroKnobRange(destination=MacroKnobDestination.OSC2_VOLUME,
                                                  start_pos=37,
                                                  end_pos=38,
                                                  depth=39),
                                   MacroKnobRange(destination=MacroKnobDestination.RING_VOLUME,
                                                  start_pos=40,
                                                  end_pos=41,
                                                  depth=42)]),
                 MacroKnob(position=43,
                           ranges=[MacroKnobRange(destination=MacroKnobDestination.NOISE_VOLUME,
                                                  start_pos=44,
                                                  end_pos=45,
                                                  depth=46),
                                   MacroKnobRange(destination=MacroKnobDestination.CUTOFF_FREQUENCY,
                                                  start_pos=47,
                                                  end_pos=48,
                                                  depth=49),
                                   MacroKnobRange(destination=MacroKnobDestination.RESONANCE,
                                                  start_pos=50,
                                                  end_pos=51,
                                                  depth=52),
                                   MacroKnobRange(destination=MacroKnobDestination.DRIVE,
                                                  start_pos=53,
                                                  end_pos=54,
                                                  depth=55)]),
                 MacroKnob(position=56,
                           ranges=[MacroKnobRange(destination=MacroKnobDestination.KEY_TRACK,
                                                  start_pos=57,
                                                  end_pos=58,
                                                  depth=59),
                                   MacroKnobRange(destination=MacroKnobDestination.ENV2_MOD,
                                                  start_pos=60,
                                                  end_pos=61,
                                                  depth=62),
                                   MacroKnobRange(destination=MacroKnobDestination.ENV1_ATTACK,
                                                  start_pos=63,
                                                  end_pos=64,
                                                  depth=65),
                                   MacroKnobRange(destination=MacroKnobDestination.ENV1_DECAY,
                                                  start_pos=66,
                                                  end_pos=67,
                                                  depth=68)]),
                 MacroKnob(position=69,
                           ranges=[MacroKnobRange(destination=MacroKnobDestination.ENV1_SUSTAIN,
                                                  start_pos=70,
                                                  end_pos=71,
                                                  depth=72),
                                   MacroKnobRange(destination=MacroKnobDestination.ENV1_RELEASE,
                                                  start_pos=73,
                                                  end_pos=74,
                                                  depth=75),
                                   MacroKnobRange(destination=MacroKnobDestination.ENV2_ATTACK,
                                                  start_pos=76,
                                                  end_pos=77,
                                                  depth=78),
                                   MacroKnobRange(destination=MacroKnobDestination.ENV2_DECAY,
                                                  start_pos=79,
                                                  end_pos=80,
                                                  depth=81)])],
    footer=Footer(eox=0xf7))

write_syx("test_patch.syx", test_patch)
p = read_syx("test_patch.syx")

d = difflib.unified_diff(pformat(p).splitlines(), pformat(test_patch).splitlines())
diff = "\n".join(d)
assert not diff, diff

# import itertools
# import re
# with open("test.py") as f:
#     text = f.read()
# vals = itertools.cycle(DistortionType)
# out = re.sub(r"\b(=DistortionType).\w+", lambda m: f"=DistortionType.{next(vals).name}", text)
# with open("test.py", "w") as f:
#     f.write(out)
