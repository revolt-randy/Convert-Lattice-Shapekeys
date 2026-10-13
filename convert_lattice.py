# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****





import bpy


def check_lattice():
# checks the current lattice object for shapekeys
# then checks for mesh objects with lattice modifier
# returns-
#   obj_list - a list of all mesh objects with lattice modifier or
#   None if no mesh object with lattice modifier not found
#

    obj_list = []    
    lattice_obj = bpy.context.object

    try:
        key_blocks = bpy.context.object.data.shape_keys.key_blocks
    except AttributeError:
        print(lattice_obj.name, " - Lattice has no shape keys")
        return None
        
    if bpy.context.object.type == 'LATTICE':
        # got lattice object - find what mesh object it's on
        for object in bpy.data.objects:
            
            if object.type == 'MESH':
                
                for mod in object.modifiers:
                    if mod.type == 'LATTICE':
                        # found mesh object with lattice modifier
                        if mod.object.name == lattice_obj.name:
                            # lattice modifier uses current lattice object
                            obj_list.append(object)

        return (obj_list)
    
    else:
        print("Lattice object not selected!")
        return None         
# end of - def check_lattice(self, context):


def apply_shapekey(dest_object):
# go thru each lattice shape key and save as shape key
# on the mesh object the lattice is modifiying
    
    shapekey_index = 0  # destination object shapekey pointer
    
    active_obj = bpy.context.view_layer.objects.active  # lattice object
    
    key_blocks = bpy.context.object.data.shape_keys.key_blocks  # lattice shapekeys
    
    bpy.context.view_layer.objects.active = bpy.data.objects[dest_object.name]  # make mesh object active
    
    # check for shapekeys on destination object
    try:
        dest_key_blocks = bpy.context.object.data.shape_keys.key_blocks  # destination object shapekeys
    except AttributeError:
        shapekey_index = 0
    else:
        # find # of shapekey on destination object
        shapekey_index = len(bpy.context.object.data.shape_keys.key_blocks) - 1 
        
    for key in key_blocks:
        if key.name == key_blocks[0].name:  # checks for 'basis' shapekey on lattice
            shapekey_index += 1
            continue

        prev_key_value = key.value
        key.value = 1
                
        bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=True, modifier="Lattice")
        
        key.value = prev_key_value
        
        bpy.data.objects[dest_object.name].active_shape_key_index = shapekey_index
        bpy.data.objects[dest_object.name].active_shape_key.name = key.name
        
        shapekey_index += 1
        
    bpy.context.view_layer.objects.active = active_obj
    
    return        
# end of - def apply_shapekey(dest_object):


class Lattice_Keys_Operator(bpy.types.Operator):
    """Convert Lattice Shape Keys to Mesh Shape Keys"""
    bl_idname = "object.lattice_keys_operator"
    bl_label = "Convert Lattice Shape Keys"

    @classmethod
    def poll(cls, context):
        return context.active_object.type == 'LATTICE'

    def execute(self, context):
        #print("\nOperator Started\n")
        
        dest_object = check_lattice()
        
        if dest_object == None:
            print("ERROR")
            self.report({'ERROR'}, "An error occurred - Check Console for details")
            return {'CANCELLED'} 
        elif len(dest_object) == 0:
            print("No mesh object with Lattice modifier found. \nERROR")
            self.report({'ERROR'}, "An error occurred - Check Console for details")
            return {'CANCELLED'}       
        else:
            for obj in dest_object:
                apply_shapekey(obj)
        
        return {'FINISHED'}
# end of - class Lattice_Keys_Operator(bpy.types.Operator):


def menu_func(self, context):
    self.layout.operator(Lattice_Keys_Operator.bl_idname, text=Lattice_Keys_Operator.bl_label, icon='PLUGIN')
    

def register():
    bpy.types.VIEW3D_MT_object_convert.append(menu_func)
    # above code causes errors.

def unregister():
    bpy.types.VIEW3D_MT_object_convert.remove(menu_func)
    





