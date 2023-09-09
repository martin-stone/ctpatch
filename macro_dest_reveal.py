from copy import deepcopy
from pathlib import Path
import ctpatch

dir = Path(r"C:\martin\docs\CircuitTracks")
base = ctpatch.read_syx(dir / "Base Bass sync.syx")

n_macro = 8
n_range = 4

for i_patch in range(2):
    out = deepcopy(base)
    for im in range(n_macro):
        for ir in range(n_range):
            idest = i_patch * n_range*n_macro + im * n_range + ir
            out.macro_knobs[im].Ranges[ir].Destination = idest
            print(idest)
    ctpatch.write_syx(dir / f"{i_patch:02}.syx", out)
