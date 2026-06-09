from pxr import Usd
import omni.usd

stage = omni.usd.get_context().get_stage()

for prim in stage.Traverse():
    if "joint" in prim.GetName().lower():
        print(prim.GetPath())
