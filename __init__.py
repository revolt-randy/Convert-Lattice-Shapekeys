bl_info = {
    "name": "Convert Lattice Shape Keys",
    "author": "revolt_randy",
    "version": (1, 1),
    "blender": (3, 6, 21),
    "location": "View3D > Object > Convert > Convert Lattice Shape Keys",
    "description": "Converts Lattice Shape Keys to Mesh Shape Keys",
    "warning": "",
    "doc_url": "https://github.com/revolt-randy/Convert-Lattice-Shapekeys",
    "tracker_url": "https://github.com/revolt-randy/Convert-Lattice-Shapekeys/issues",
    "category": "Object",
}



# Import From Files
if "bpy" in locals():
    import importlib
    importlib.reload(convert_lattice)
else:
    from .import convert_lattice

    
import bpy
from . import convert_lattice
    

# Register and add to the "object -> convert" menu (required to also use F3 search "Convert Lattice Shape Keys" for quick access).
def register():
    bpy.utils.register_class(convert_lattice.Lattice_Keys_Operator)
    convert_lattice.register()
    # above code causes errors.

def unregister():
    bpy.utils.unregister_class(convert_lattice.Lattice_Keys_Operator)
    convert_lattice.unregister()
    

if __name__ == "__main__":
    register()

