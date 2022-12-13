from pathlib import Path
import sys
import time
import rtmidi
import ctpatch


def main():
    if len(sys.argv) > 1:
        print(f"Reading file {sys.argv[1]}")
        bank = Path(sys.argv[1]).read_bytes()
        patches = [bank[i:i+ctpatch.PATCH_BYTES] for i in range(0, len(bank), ctpatch.PATCH_BYTES)]
        assert all(patch[0] == 0xf0 and patch[-1] == 0xf7 for patch in patches)
        with ct_out() as midiout:
            for i, patch in enumerate(patches):

                ctp = ctpatch.decode(patch)
                print(ctp.meta.name)
                ctp.command = ctpatch.ReplacePatchCommand(pack_index=1, patch_index=i)

                sysex = ctpatch.encode(ctp)
                print(f"Sending {len(sysex)} bytes. {i+1} of {len(patches)}")
                midiout.send_message(sysex)
                time.sleep(0.5)

    # current = get_current_patch()
    # print(current.patch.Name.decode("utf8"))


def write_sysex():
    if len(sys.argv) > 1:
        print(f"Reading file {sys.argv[1]}")
        sysex = Path(sys.argv[1]).read_bytes()
        assert sysex[0] == 0xf0 and sysex[-1] == 0xf7
        with ct_out() as midiout:
            print(f"Sending {len(sysex)} bytes.")
            midiout.send_message(sysex)
            time.sleep(0.5)


def get_current_patch():
    with ct_in() as midiin, ct_out() as midiout:
        # midiin.set
        print("Sending...")
        midiout.send_message(ctpatch.encode(ctpatch.PatchDumpRequest()))
        print("Waiting for response...")
        while True:
            msg = midiin.get_message()
            if msg:
                message, deltatime = msg
                if message[0] == 0xf0 and message[-1] == 0xf7:
                    return ctpatch.decode(bytes(message))
            time.sleep(0.01)


def ct_out():
    midiout = rtmidi.MidiOut()
    out_index = circuit_port(midiout)
    midiout.open_port(out_index)
    return midiout


def ct_in():
    midiin = rtmidi.MidiIn()
    in_index = circuit_port(midiin)
    midiin.open_port(in_index)
    midiin.ignore_types(sysex=False)
    return midiin


def circuit_port(midi):
    ports: list = midi.get_ports()
    return next(i for i, name in enumerate(ports) if "Circuit Tracks" in name)


def note():
    on = bytes([0b10010000, 0x30, 0x7f])
    off = bytes([0b10000000, 0x30, 0x7f])
    with ct_out() as midiout:
        midiout.send_message(on)
        time.sleep(1)
        midiout.send_message(off)
        time.sleep(0.1)


if __name__ == "__main__":
    main()
    # p = get_current_patch()
    # print(p.patch.Name)
    # note()
    # write_sysex()
