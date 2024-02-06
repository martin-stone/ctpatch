from copy import deepcopy
from itertools import product
from pathlib import Path
# from pprint import pprint
import ctpatch

patches_per_page = 32

def main():
    base_filename = Path(r"~/Documents/CircuitTracks/Saw Pad.syx").expanduser()
    out_dir = Path(r"~/Documents/CircuitTracks").expanduser()
    base = ctpatch.read_syx(base_filename)

    start_index = patches_per_page * 1
    indexed_patches = [(i+start_index, p) for i, p in combinations(base)]
    for i, p in indexed_patches:
        name = p.meta.name.decode('utf8').strip()
        ctpatch.write_syx(out_dir / f"{i:02} {name}.syx", p)

    patch_range = min(i for i, _ in indexed_patches), max(i for i, _ in indexed_patches)
    bank = concat_bank(indexed_patches)
    (out_dir / f"bank-pad-{patch_range[0]:02}-{patch_range[1]:02}.syx").write_bytes(bank)


def combinations(base: ctpatch.PatchSysex):

    dimensions = [
        (
            # shape
            (0b0, (osc_saw,), "saw"),
            (0b1, (osc_square,), "squ"),
        ),
        (
            # Osc2 interval
            (0b00, (osc_unison,), "0"),
            (0b10, (osc_5th,), "5")
        ),
        (
            # Noise level
            (0b000, (noise,), "noise"),
            (0b100, (quiet,), "quiet")
        ),
    ]

    def apply(combination, base):
        out = deepcopy(base)
        index = sum(n for n, _, _ in combination)
        name = "Pad " + " ".join(s for _, _, s in combination)
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


def osc_saw(p: ctpatch.PatchSysex):
    p.oscillators[0].wave = ctpatch.OscWaveform.SAWTOOTH  # XXX no pwm
    p.oscillators[0].pulse_width_index = 0


def osc_square(p: ctpatch.PatchSysex):
    p.oscillators[0].wave = ctpatch.OscWaveform.PULSE_WIDTH
    p.oscillators[0].pulse_width_index = 0x40


def osc_unison(p: ctpatch.PatchSysex):
    p.oscillators[1].semitones += 0


def osc_5th(p: ctpatch.PatchSysex):
    p.oscillators[1].semitones += 7


def noise(p: ctpatch.PatchSysex):
    p.mixer.noise_level = 20


def quiet(p: ctpatch.PatchSysex):
    p.mixer.noise_level = 0


if __name__ == "__main__":
    main()
