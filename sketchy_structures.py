bl_info = {
    'name': 'Sketchy Structures',
    'category': 'Mesh',
}

import bpy, bmesh

def create_edges(context):
    edit_object = bpy.context.object
    edit_mesh = bmesh.from_edit_mesh(edit_object.data)
    selected_verts = [vert for vert in edit_mesh.verts if vert.select]
    created_edges = []

    for i, vertA in enumerate(selected_verts):
        for vertB in selected_verts[i + 1:]:
            dist = (vertB.co - vertA.co).length
            if dist > 0.0 and not edge_exists(edit_mesh, vertA, vertB):
                edge = add_edge(edit_mesh, vertA, vertB)
                created_edges.append(edge)

    bmesh.update_edit_mesh(edit_object.data)
    return {'edges': created_edges}

# TODO: Possible to optimize with a weak map or simpler lookup?
def edge_exists(mesh, v0, v1):
    existing_edges = [edge for edge in mesh.edges if v0 in edge.verts and v1 in edge.verts]
    return len(existing_edges) > 0

def add_edge(mesh, v0, v1):
    return mesh.edges.new((v0, v1))

class SketchyStructuresOperator(bpy.types.Operator):
    """Sketchy Structures"""
    bl_idname = 'mesh.sketchy_structures_operator'
    bl_label = 'Sketchy Structures'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        res = create_edges(context)
        self.report({'INFO'}, 'Created %s edges' % len(res['edges']))
        return {'FINISHED'}

def draw_menu(self, context):
    self.layout.operator(SketchyStructuresOperator.bl_idname)

def register():
    bpy.utils.register_class(SketchyStructuresOperator)
    bpy.types.VIEW3D_MT_edit_mesh_edges.append(draw_menu)

def unregister():
    bpy.utils.unregister_class(SketchyStructuresOperator)
    bpy.types.VIEW3D_MT_edit_mesh_edges.remove(draw_menu)

if __name__ == "__main__":
    register()
