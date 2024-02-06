from copy import deepcopy
from itertools import product
from pathlib import Path
# from pprint import pprint
import ctpatch


def main():
    base_filename = Path(r"~/Documents/CircuitTracks/Base Bass.syx").expanduser()
    out_dir = Path(r"~/Documents/CircuitTracks").expanduser()
    base = ctpatch.read_syx(base_filename)

    indexed_patches = combinations(base)
    for i, p in indexed_patches:
        name = p.meta.name.decode('utf8').strip()
        ctpatch.write_syx(out_dir / f"{i:02} {name}.syx", p)

    patch_range = min(i for i, _ in indexed_patches), max(i for i, _ in indexed_patches)
    bank = concat_bank(indexed_patches)
    (out_dir / f"bank-bass-{patch_range[0]:02}-{patch_range[1]:02}.syx").write_bytes(bank)


def combinations(base: ctpatch.PatchSysex):

    dimensions = [
        (
            # shape & lfo
            (0b000, (osc_saw, lfo_filter), "saw"),
            (0b001, (osc_square, lfo_filter), "squ"),
            (0b010, (osc_sin_tri, lfo_sync), "sync"),
            (0b011, (osc_vocal, lfo_pwm), "voc")
        ),
        (
            # fx knob
            (0b000, (fx_dist, ), "dst"),
            (0b100, (fx_sync,), "syn")
        ),
    ]

    def apply(combination, base):
        out = deepcopy(base)
        index = sum(n for n, _, _ in combination)
        name = " ".join(s for _, _, s in combination)
        for _, funcs, _ in combination:
            for func in funcs:
                func(out)
        out.meta.name = name.encode("utf8")
        return index, out

    indexed_patches = sorted(apply(c, base) for c in product(*dimensions))
    return indexed_patches


def concat_bank(indexed_patches):
    for i, p in indexed_patches:
        p.header.command = ctpatch.SysexCommand.REPLACE_PATCH
        p.header.location = i
    return b"".join(ctpatch.encode(p) for i, p in indexed_patches)


def fx_dist(p: ctpatch.PatchSysex):
    p.macro_knobs[7].ranges[0].destination = ctpatch.MacroKnobDestination.DISTORTION_LEVEL


def fx_sync(p: ctpatch.PatchSysex):
    p.macro_knobs[7].ranges[0].destination = ctpatch.MacroKnobDestination.O1_VSYNC_DEPTH


def lfo_sync(p: ctpatch.PatchSysex):
    p.mod_matrix[0].destination = ctpatch.ModMatrixDestination.OSC_1_V_SYNC
    p.mod_matrix[0].source1 = ctpatch.ModMatrixSource.LFO_1_PLUS


def lfo_filter(p: ctpatch.PatchSysex):
    p.mod_matrix[0].destination = ctpatch.ModMatrixDestination.FILTER_FREQUENCY
    p.mod_matrix[0].source1 = ctpatch.ModMatrixSource.LFO_1_PLUS


def lfo_pwm(p: ctpatch.PatchSysex):
    p.mod_matrix[0].destination = ctpatch.ModMatrixDestination.OSC_1_PULSE_WIDTH_INDEX


def osc_saw(p: ctpatch.PatchSysex):
    p.oscillators[0].wave = ctpatch.OscWaveform.SAWTOOTH  # XXX no pwm
    p.oscillators[0].pulse_width_index = 0


def osc_square(p: ctpatch.PatchSysex):
    p.oscillators[0].wave = ctpatch.OscWaveform.PULSE_WIDTH
    p.oscillators[0].pulse_width_index = 0x40


def osc_sin_tri(p: ctpatch.PatchSysex):
    p.oscillators[0].wave = ctpatch.OscWaveform.SINE
    p.oscillators[1].wave = ctpatch.OscWaveform.TRIANGLE
    p.mixer.osc2_level = 127


def osc_vocal(p: ctpatch.PatchSysex):
    p.oscillators[0].wave = ctpatch.OscWaveform.DIGITAL_VOCAL_6
    p.oscillators[0].pulse_width_index = 0


if __name__ == "__main__":
    main()
