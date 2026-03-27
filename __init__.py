bl_info = {
    "name": "BB Parent to Empty",
    "author": "BB",
    "version": (1, 0),
    "blender": (4, 5, 0),
    "location": "Object > Parent > Parent to Empty",
    "description": "Parents selected objects to a new Empty named after the active object",
    "category": "Object",
}

import bpy


class BB_OT_ParentToEmpty(bpy.types.Operator):
    bl_idname = "bb.parent_to_empty"
    bl_label = "Parent to Empty"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and len(context.selected_objects) > 0

    def execute(self, context):
        active = context.active_object
        selected = context.selected_objects

        empty_name = f"{active.name}_gp"
        print(f"[BB] Creating empty '{empty_name}'")

        empty = bpy.data.objects.new(empty_name, None)
        empty.empty_display_type = 'PLAIN_AXES'
        empty.location = active.location.copy()
        context.collection.objects.link(empty)
        context.view_layer.update()

        print(f"[BB] Parenting {[o.name for o in selected]} to '{empty_name}'")

        for obj in selected:
            mat = obj.matrix_world.copy()
            obj.parent = empty
            obj.matrix_world = mat

        for obj in selected:
            obj.select_set(False)
        empty.select_set(True)
        context.view_layer.objects.active = empty

        print(f"[BB] Done")
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(BB_OT_ParentToEmpty.bl_idname)


def register():
    bpy.utils.register_class(BB_OT_ParentToEmpty)
    bpy.types.VIEW3D_MT_object_parent.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object_parent.remove(menu_func)
    bpy.utils.unregister_class(BB_OT_ParentToEmpty)


if __name__ == "__main__":
    register()
