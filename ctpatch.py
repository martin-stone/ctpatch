"""
Read, modify and write .syx patch files for the Novation Circuit Tracks.
"""

from ctypes import Structure, c_ubyte
from dataclasses import dataclass, field, fields, is_dataclass
from enum import IntEnum
from pathlib import Path
import struct


@dataclass
class BytesBuf:
    buffer: bytes
    read_offset: int = 0

    def unpack(self, format):
        vals = struct.unpack_from(format, self.buffer, self.read_offset)
        self.read_offset += struct.calcsize(format)
        return vals


def format(format: str) -> dict:
    def decode(field_type, buff: BytesBuf):
        return field_type(*buff.unpack(format))
    return dict(metadata=dict(
        decode=decode,
        encode=lambda obj: struct.pack(format, obj)))


def bitfield(format: str = "1s") -> dict:
    def decode(field_type, buff: BytesBuf):
        return field_type.from_buffer_copy(buff.unpack(format)[0])
    return dict(metadata=dict(
        decode=decode,
        encode=bytearray))


def list_len(length: int) -> dict:
    def decode(field_type, buff: BytesBuf):
        item_type = field_type.__args__[0]
        return list((_decode(item_type, {}, buff) for _ in range(length)))

    def encode(obj_list):
        return b"".join(_encode(obj, {}) for obj in obj_list)

    return dict(metadata=dict(decode=decode, encode=encode))


def read_type(field_type) -> dict:
    def decode(_, buff: BytesBuf):
        return _decode(field_type, {}, buff)
    return dict(metadata=dict(
        decode=decode,
        encode=lambda obj: _encode(obj, {})))


PATCH_BYTES = 350
NOVATION_ID = b"\x00\x20\x29"
CIRCUIT_TRACKS_ID = 0x64
CIRCUIT_ORIGINAL_ID = 0x60


class SysexCommand(IntEnum):
    REPLACE_CURRENT_PATCH = 0
    REPLACE_PATCH = 1
    REQUEST_DUMP_CURRENT_PATCH = 0x40


class PolyphonyMode(IntEnum):
    MONO = 0
    MONO_AG = 1
    POLY = 2


class OscWaveform(IntEnum):
    SINE = 0
    TRIANGLE = 1
    SAWTOOTH = 2
    SAW_9_1_PW = 3
    SAW_8_2_PW = 4
    SAW_7_3_PW = 5
    SAW_6_4_PW = 6
    SAW_5_5_PW = 7
    SAW_4_6_PW = 8
    SAW_3_7_PW = 9
    SAW_2_8_PW = 10
    SAW_1_9_PW = 11
    PULSE_WIDTH = 12
    SQUARE = 13
    SINE_TABLE = 14
    ANALOGUE_PULSE = 15
    ANALOGUE_SYNC = 16
    TRIANGLE_SAW_BLEND = 17
    DIGITAL_NASTY_1 = 18
    DIGITAL_NASTY_2 = 19
    DIGITAL_SAW_SQUARE = 20
    DIGITAL_VOCAL_1 = 21
    DIGITAL_VOCAL_2 = 22
    DIGITAL_VOCAL_3 = 23
    DIGITAL_VOCAL_4 = 24
    DIGITAL_VOCAL_5 = 25
    DIGITAL_VOCAL_6 = 26
    RANDOM_COLLECTION_1 = 27
    RANDOM_COLLECTION_2 = 28
    RANDOM_COLLECTION_3 = 29


class LfoWaveform(IntEnum):
    SINE = 0
    TRIANGLE = 1
    SAWTOOTH = 2
    SQUARE = 3
    RANDOM_S_H = 4
    TIME_S_H = 5
    PIANO_ENVELOPE = 6
    SEQUENCE_1 = 7
    SEQUENCE_2 = 8
    SEQUENCE_3 = 9
    SEQUENCE_4 = 10
    SEQUENCE_5 = 11
    SEQUENCE_6 = 12
    SEQUENCE_7 = 13
    ALTERNATIVE_1 = 14
    ALTERNATIVE_2 = 15
    ALTERNATIVE_3 = 16
    ALTERNATIVE_4 = 17
    ALTERNATIVE_5 = 18
    ALTERNATIVE_6 = 19
    ALTERNATIVE_7 = 20
    ALTERNATIVE_8 = 21
    CHROMATIC = 22
    CHROMATIC_16 = 23
    MAJOR = 24
    MAJOR_7 = 25
    MINOR_7 = 26
    MIN_ARP_1 = 27
    MIN_ARP_2 = 28
    DIMINISHED = 29
    DEC_MINOR = 30
    MINOR_3RD = 31
    PEDAL = 32
    _4THS = 33
    _4THS_X12 = 34
    _1625_MAJ = 35
    _1625_MIN = 36
    _2511 = 37


class LfoFadeMode(IntEnum):
    FADE_IN = 0
    FADE_OUT = 1
    GATE_IN = 2
    GATE_OUT = 3


class MacroKnobDestination(IntEnum):
    NO_DESTINATION = 0
    PORTAMENTO_RATE = 1
    POST_FX_VOLUME = 2
    O1_WAVE_INTERPOLATE = 3
    O1_PULSE_WIDTH_INDEX = 4
    O1_VSYNC_DEPTH = 5
    O1_DENSITY = 6
    O1_DENSITY_DETUNE = 7
    O1_SEMITONES_TUNE = 8
    O1_CENTS_TUNE = 9
    O2_WAVE_INTERPOLATE = 10
    O2_PULSE_WIDTH_INDEX = 11
    O2_VSYNC_DEPTH = 12
    O2_DENSITY = 13
    O2_DENSITY_DETUNE = 14
    O2_SEMITONES_TUNE = 15
    O2_CENTS_TUNE = 16
    OSC1_VOLUME = 17
    OSC2_VOLUME = 18
    RING_VOLUME = 19
    NOISE_VOLUME = 20
    CUTOFF_FREQUENCY = 21
    RESONANCE = 22
    DRIVE = 23
    KEY_TRACK = 24
    ENV2_MOD = 25
    ENV1_ATTACK = 26
    ENV1_DECAY = 27
    ENV1_SUSTAIN = 28
    ENV1_RELEASE = 29
    ENV2_ATTACK = 30
    ENV2_DECAY = 31
    ENV2_SUSTAIN = 32
    ENV2_RELEASE = 33
    ENV3_DELAY = 34
    ENV3_ATTACK = 35
    ENV3_DECAY = 36
    ENV3_SUSTAIN = 37
    ENV3_RELEASE = 38
    LFO1_RATE = 39
    LFO1_SYNC = 40
    LFO1_SLEW = 41
    LFO2_RATE = 42
    LFO2_SYNC = 43
    LFO2_SLEW = 44
    DISTORTION_LEVEL = 45
    CHORUS_LEVEL = 46
    CHORUS_RATE = 47
    CHORUS_FEEDBACK = 48
    CHORUS_DEPTH = 49
    CHORUS_DELAY = 50
    MOD_MATRIX_01 = 51
    MOD_MATRIX_02 = 52
    MOD_MATRIX_03 = 53
    MOD_MATRIX_04 = 54
    MOD_MATRIX_05 = 55
    MOD_MATRIX_06 = 56
    MOD_MATRIX_07 = 57
    MOD_MATRIX_08 = 58
    MOD_MATRIX_09 = 59
    MOD_MATRIX_10 = 60
    MOD_MATRIX_11 = 61
    MOD_MATRIX_12 = 62
    MOD_MATRIX_13 = 63
    MOD_MATRIX_14 = 64
    MOD_MATRIX_15 = 65
    MOD_MATRIX_16 = 66
    MOD_MATRIX_17 = 67
    MOD_MATRIX_18 = 68
    MOD_MATRIX_19 = 69
    MOD_MATRIX_20 = 70


class ModMatrixSource(IntEnum):
    DIRECT = 0
    VELOCITY = 4
    KEYBOARD = 5
    LFO_1_PLUS = 6
    LFO_1_PLUS_MINUS = 7
    LFO_2_PLUS = 8
    LFO_2_PLUS_MINUS = 9
    ENV_AMP = 10
    ENV_FILTER = 11


class ModMatrixDestination(IntEnum):
    OSC_1_AND_2_PITCH = 0
    OSC_1_PITCH = 1
    OSC_2_PITCH = 2
    OSC_1_V_SYNC = 3
    OSC_2_V_SYNC = 4
    OSC_1_PULSE_WIDTH_INDEX = 5
    OSC_2_PULSE_WIDTH_INDEX = 6
    OSC_1_LEVEL = 7
    OSC_2_LEVEL = 8
    NOISE_LEVEL = 9
    RING_MODULATION_LEVEL = 10
    FILTER_DRIVE_AMOUNT = 11
    FILTER_FREQUENCY = 12
    FILTER_RESONANCE = 13
    LFO_1_RATE = 14
    LFO_2_RATE = 15
    AMP_ENVELOPE_DECAY = 16
    FILTER_ENVELOPE_DECAY = 17


class DistortionType(IntEnum):
    DIODE = 0
    VALVE = 1
    CLIPPER = 2
    CROSS_OVER = 3
    RECTIFIER = 4
    BIT_REDUCER = 5
    RATE_REDUCER = 6


class FilterType(IntEnum):
    LOW_PASS_12DB = 0
    LOW_PASS_24DB = 1
    BAND_PASS_6DB = 2
    BAND_PASS_12DB = 3
    HIGH_PASS_12DB = 4
    HIGH_PASS_24DB = 5


@dataclass
class Header:
    sysex: int = 0xf0
    mfr_id: bytes = field(default=NOVATION_ID, **format("3s"))
    prod_type: int = 0x01
    prod_num: int = CIRCUIT_TRACKS_ID


@dataclass
class ReplaceCurrentPatchCommand:
    command_id: int = SysexCommand.REPLACE_CURRENT_PATCH
    location: int = 0
    _reserved: int = 0


@dataclass
class ReplacePatchCommand:
    command_id: int = SysexCommand.REPLACE_PATCH
    pack_index: int = field(default=0, **format("<H"))
    patch_index: int = 0
    _reserved: int = 0


@dataclass
class Meta:
    _name: bytes = field(**format("16s"))
    category: int = 0
    genre: int = 0
    _reserved: bytes = field(default=b"\x00"*14, **format("14s"))

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: bytes):
        if len(value) > 16:
            raise ValueError(f"Name is limited to 16 bytes. (Given '{value}' {len(value)})")
        self._name = value + b" " * (16 - len(value))


@dataclass
class Voice:
    polyphony_mode: PolyphonyMode
    portamento_rate: int
    pre_glide: int
    keyboard_octave: int


@dataclass
class Osc:
    wave: OscWaveform
    wave_interpolate: int
    pulse_width_index: int
    virtual_sync_depth: int
    density: int
    density_detune: int
    semitones: int
    cents: int
    pitch_bend: int


@dataclass
class Mixer:
    osc1_level: int
    osc2_level: int
    ring_mod_level12: int
    noise_level: int
    pre_fx_level: int
    post_fx_level: int


@dataclass
class Filter:
    routing: int
    drive: int
    drive_type: DistortionType
    type: FilterType
    frequency: int
    track: int
    resonance: int
    q_normalise: int
    env2_to_freq: int


@dataclass
class Envelope:
    velocity_or_delay: int
    attack: int
    decay: int
    sustain: int
    release: int


class LfoFlags(Structure):
    _fields_ = [
        ("one_shot", c_ubyte, 1),
        ("key_sync", c_ubyte, 1),
        ("common_sync", c_ubyte, 1),
        ("delay_trigger", c_ubyte, 1),
        ("fade_mode", c_ubyte, 4)
    ]

    def __repr__(self):
        return "LfoFlags(" + ", ".join(f"{k}={getattr(self, k)}" for k, t, b in self._fields_) + ")"


@dataclass
class Lfo:
    waveform: LfoWaveform
    phase_offset: int
    slew_rate: int
    delay: int
    delay_sync: int
    rate: int
    rate_sync: int
    flags: LfoFlags = field(**bitfield())


@dataclass
class Fx:
    distortion_level: int
    _fx_reserved1: int
    chorus_level: int
    _fx_reserved2: int
    _fx_reserved3: int
    equaliser_bass_frequency: int
    equaliser_bass_level: int
    equaliser_mid_frequency: int
    equaliser_mid_level: int
    equaliser_treble_frequency: int
    equaliser_treble_level: int
    _fx_reserved45678: bytes = field(**format("5s"))
    distortion_type: DistortionType
    distortion_compensation: int
    chorus_type: int
    chorus_rate: int
    chorus_rate_sync: int
    chorus_feedback: int
    chorus_mod_depth: int
    chorus_delay: int


@dataclass
class ModMatrix:
    source1: ModMatrixSource
    source2: ModMatrixSource
    depth: int
    destination: ModMatrixDestination


@dataclass
class MacroKnobRange:
    destination: MacroKnobDestination
    start_pos: int
    end_pos: int
    depth: int


@dataclass
class MacroKnob:
    position: int
    ranges: list[MacroKnobRange] = field(**list_len(4))


@dataclass
class Footer:
    eox: int = 0xf7


@dataclass
class PatchSysex:
    header: Header
    command: ReplaceCurrentPatchCommand | ReplacePatchCommand = field(**read_type(ReplaceCurrentPatchCommand))
    meta: Meta
    voice: Voice
    oscillators: list[Osc] = field(**list_len(2))
    mixer: Mixer
    filter: Filter
    envelopes: list[Envelope] = field(**list_len(3))
    lfos: list[Lfo] = field(**list_len(2))
    fx: Fx
    mod_matrix: list[ModMatrix] = field(**list_len(20))
    macro_knobs: list[MacroKnob] = field(**list_len(8))
    footer: Footer


@dataclass
class CurrentPatchDumpRequestCommand:
    command_id: int = SysexCommand.REQUEST_DUMP_CURRENT_PATCH
    location: int = 0


@dataclass
class PatchDumpRequest:
    header: Header = field(default_factory=Header)
    command: CurrentPatchDumpRequestCommand = field(default_factory=CurrentPatchDumpRequestCommand)
    footer: Footer = field(default_factory=Footer)


def read_syx(syx_filename: str | Path) -> PatchSysex:
    with open(syx_filename, "rb") as f:
        buffer = f.read()
    assert len(buffer) == PATCH_BYTES
    patch = decode(buffer)
    validate(patch)
    return patch


def write_syx(syx_filename: str | Path, patch: PatchSysex):
    validate(patch)
    bytes = encode(patch)
    assert len(bytes) == PATCH_BYTES
    with open(syx_filename, "wb") as f:
        f.write(bytes)


def validate(patch: PatchSysex):
    assert patch.header.mfr_id == NOVATION_ID
    assert patch.header.prod_num in (CIRCUIT_TRACKS_ID, CIRCUIT_ORIGINAL_ID)
    assert len(patch.oscillators) == 2
    assert len(patch.envelopes) == 3
    assert len(patch.mod_matrix) == 20
    assert len(patch.macro_knobs) == 8
    assert patch.footer.eox == 0xf7


def decode(buffer: bytes) -> PatchSysex:
    read_buf = BytesBuf(buffer)
    return _decode(PatchSysex, {}, read_buf)


def _decode(field_type, metadata, read_buf: BytesBuf):
    if metadata:
        return metadata["decode"](field_type, read_buf)
    elif is_dataclass(field_type):
        fs = fields(field_type)
        return field_type(*(_decode(f.type, f.metadata, read_buf) for f in fs))
    else:
        # If no metadata & not a dataclass, read a byte into an int or enum
        return field_type(*read_buf.unpack("B"))


def encode(obj) -> bytes:
    return _encode(obj, {})


def _encode(obj, metadata) -> bytes:
    if metadata:
        return metadata["encode"](obj)
    elif is_dataclass(obj):
        return b"".join(_encode(getattr(obj, f.name), f.metadata) for f in fields(obj))
    else:
        # If no metadata & not a dataclass, pack an int or enum into a byte
        return struct.pack("B", obj)
