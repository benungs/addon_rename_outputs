bl_info = {
    "name"        : "Output Renamer",
    "author"      : "Ben U",
    "description" : "Search/Replace text for ALL render outputs (including the compositor)",
    "blender"     : (3, 4, 0),
    "version"     : (1, 0),
    "category"    : "Render",
}

import bpy


# ====== Function ======

def rename_outputs():
    
    old_str = bpy.context.scene.renamer_tool.search_str
    new_str = bpy.context.scene.renamer_tool.replace_str

    for scene in bpy.data.scenes:
        # FIRST rename 'File Output' nodes (if they exist)
        if scene.use_nodes:
            for node in scene.node_tree.nodes:
                if node.type == 'OUTPUT_FILE':
                    node.base_path = node.base_path.replace(old_str, new_str)
                    slot_count = len(node.file_slots.items());
                    for i in range(slot_count):
                        node.file_slots[i].path = node.file_slots[i].path.replace(old_str, new_str)
        # SECOND rename the standard 'Output' 
        scene.render.filepath = scene.render.filepath.replace(old_str, new_str)
        
# ====== Panel ====== 

class MyProperties(bpy.types.PropertyGroup):
    search_str : bpy.props.StringProperty(name="Search", description="The stuff you want to remove")
    replace_str : bpy.props.StringProperty(name="Replace", description= "The stuff you want to replace it with")


class renamer_panel(bpy.types.Panel):
    bl_label = "Output Renamer"
    bl_idname = "OBJECT_PT_renamer_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        renamertool = scene.renamer_tool
        
        layout.prop(renamertool, "search_str")
        layout.prop(renamertool, "replace_str")

        row = layout.row()
        row.operator("opr.operator")

       
class renamer_operator(bpy.types.Operator):
    bl_idname = 'opr.operator'
    bl_label = 'Rename Outputs'
    bl_description = "Run a Search & Replace on all output directories and filenames. This only affects future renders; it does not modify existing file and directory names."
    
    def execute(self, context):
        rename_outputs()
        return {'FINISHED'}


def register():
    bpy.utils.register_class(renamer_panel)
    bpy.utils.register_class(MyProperties)
    bpy.utils.register_class(renamer_operator)
    
    bpy.types.Scene.renamer_tool = bpy.props.PointerProperty(type= MyProperties)


def unregister():
    bpy.utils.unregister_class(renamer_panel)
    bpy.utils.unregister_class(MyProperties)
    bpy.utils.unregister_class(renamer_operator)
    
    del bpy.types.Scene.renamer_tool

if __name__ == "__main__":
    register()