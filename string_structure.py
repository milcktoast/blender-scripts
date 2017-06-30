import bpy, bmesh

def main(context):
    edit_object = bpy.context.object
    edit_mesh = bmesh.from_edit_mesh(edit_object.data)
    selected_verts = [v for v in edit_mesh.verts if v.select]

    for i, vertA in enumerate(selected_verts):
        for vertB in selected_verts[i + 1:]:
            dist = (vertB.co - vertA.co).length
            if dist > 0.0:
                add_edge(edit_mesh, vertA, vertB)

    bmesh.update_edit_mesh(edit_object.data)

# FIXME: Check if edge exists first
def add_edge(mesh, v0, v1):
    try:
        mesh.edges.new((v0, v1))
    except Exception as err:
        print(err, v0, v1)

class StringStructureOperator(bpy.types.Operator):
    bl_idname = 'object.string_structure_operator'
    bl_label = 'String Structure'

    def execute(self, context):
        main(context)
        return {'FINISHED'}

bpy.utils.register_class(StringStructureOperator)
try:
    bpy.ops.object.string_structure_operator()
except Exception as err:
    raise err
