import difflib
import pprint
import sys
import ctpatch


patch_files = sys.argv[1:3]

patch_objs = [ctpatch.read_syx(fn) for fn in patch_files]
pretty_patches = [pprint.pformat(obj).splitlines() for obj in patch_objs]
diff = difflib.unified_diff(pretty_patches[0], pretty_patches[1], fromfile=patch_files[0], tofile=patch_files[1])
print("\n".join(diff))

