import time
import ctpatch

"""
Example usage.
Read example.syx and generate programmatically modified versions of it.
"""

patch = ctpatch.read_syx("example.syx")

# Save a modified version of the input patch for every filter type.
for type in ctpatch.FilterType:
    name = type.name
    # Set the patch values...
    # Patch name is the filter type (converted to bytes)
    patch.meta.name = name.encode("utf8")
    patch.filter.type = type
    # Write the file
    filename = f"generated {name}.syx"
    print(f"Saving patch '{filename}'...")
    ctpatch.write_syx(filename, patch)


"""
Example of how you'd upload the above patch files to CircuitTracks automatically:
(Close Components or this will fail.)
"""

# (Disabled by default -- Will overwrite what's there.)
upload_patches = False

if upload_patches:
    # Third-party library, python-rtmidi:
    import rtmidi

    # zero-based pack index
    pack_index = 1

    patch_slot_file_names = (
        # patch numbers to put them in the second row (zero-based)
        (8, "generated LOW_PASS_12DB.syx"),
        (9, "generated LOW_PASS_24DB.syx"),
        (10, "generated BAND_PASS_6DB.syx"),
        (11, "generated BAND_PASS_12DB.syx"),
        (12, "generated HIGH_PASS_12DB.syx"),
        (13, "generated HIGH_PASS_24DB.syx"),
    )

    # Open the CT midi port.
    # Failures here usually mean CT is not connected, or Components is already connected to CT.
    midiout = rtmidi.MidiOut()
    out_index = next(i for i, name in enumerate(midiout.get_ports()) if "Circuit Tracks" in name)
    midiout.open_port(out_index)

    for slot, name in patch_slot_file_names:
        patch = ctpatch.read_syx(name)
        # To write a patch, the sysex command must be set to a ReplacePatchCommand
        patch.command = ctpatch.ReplacePatchCommand(pack_index=pack_index, patch_index=slot)

        sysex_bytes = ctpatch.encode(patch)
        print(f"Sending '{name}' to MIDI output {out_index} ...")
        midiout.send_message(sysex_bytes)
        # Let CT catch up...
        time.sleep(0.1)
