import bpy
from bpy.types import WorkSpaceTool
from bpy_extras import view3d_utils

def main(context, event):
    
    scene = context.scene
    region = context.region
    rv3d = context.region_data
    coord = event.mouse_region_x, event.mouse_region_y
    viewlayer = context.view_layer
    depsgraph = context.evaluated_depsgraph_get()

    # get the ray from the viewport and mouse
    view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
    ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
    
    result, location, normal, index, object, matrix = scene.ray_cast(viewlayer, ray_origin, view_vector)  

    if object:
        wmtx = object.matrix_world    
        object_eval = object.evaluated_get(depsgraph)    
        
        if context.mode=='OBJECT':            
                        
            face=object_eval.data.polygons[index]  
            loc = wmtx @ face.center   
            
        else:  
            mesh_from_eval = bpy.data.meshes.new_from_object(object_eval)
            
            face=mesh_from_eval.polygons[index]
            loc = wmtx @ face.center 
        
        bpy.context.scene.cursor.location=loc    

    return {'FINISHED'}


class FACE_OT_center(bpy.types.Operator):
    bl_idname = "view3d.face_center"
    bl_label = "snap cursor 2 face center-sfc"     
    
    @classmethod
    def poll(cls, context):
        return context.mode in {'OBJECT','EDIT_MESH'}

    def modal(self, context, event):        
        
        
 
        if event.type == 'MOUSEMOVE':
            
            bpy.ops.view3d.cursor3d('INVOKE_DEFAULT',use_depth=False, orientation='GEOM')
            main(context, event)  
            return {'FINISHED'}
        
#        elif event.type == 'LEFTMOUSE' and event.value == 'PRESS':
#                return {'FINISHED'}
        
#        elif event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE','TAB'}:
#            # allow navigation
#            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):    
    
        self.cursor_loc=bpy.context.scene.cursor.location.copy()
        self.cursor_rot=bpy.context.scene.cursor.rotation_euler.copy()
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}        



class Center_snap_obj(WorkSpaceTool):
    bl_space_type = 'VIEW_3D'
    bl_context_mode = 'OBJECT'

    # The prefix of the idname should be your add-on name.
    bl_idname = "my_template.my_circle_select"
    bl_label = "MY snap cursor"
    bl_description = (
        "Snap the cursor\n to face center"
        
    )
    bl_icon = "ops.generic.cursor"
    bl_widget = None
    bl_keymap = (
        ("view3d.face_center", {"type": 'LEFTMOUSE', "value": 'PRESS'},
         {"properties": [("wait_for_input", False)]}),

    )
class Center_snap_edit(WorkSpaceTool):
    bl_space_type = 'VIEW_3D'
    bl_context_mode = 'EDIT_MESH'

    # The prefix of the idname should be your add-on name.
    bl_idname = "my_template.my_circle_select"
    bl_label = "MY snap cursor"
    bl_description = (
        "Snap the cursor\n to face center"
        
    )
    bl_icon = "ops.generic.cursor"
    bl_widget = None
    bl_keymap = (
        ("view3d.face_center", {"type": 'LEFTMOUSE', "value": 'PRESS'},
         {"properties": [("wait_for_input", False)]}),

    )

def register():
    bpy.utils.register_class(FACE_OT_center)
    bpy.utils.register_tool(Center_snap_obj)
    bpy.utils.register_tool(Center_snap_edit)


def unregister():
    bpy.utils.unregister_class(FACE_OT_center)
    bpy.utils.unregister_tool(Center_snap_obj)
    bpy.utils.unregister_tool(Center_snap_edit)



if __name__ == "__main__":
    register()
