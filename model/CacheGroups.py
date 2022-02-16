import bpy


class MeshObjectCache(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Mesh Object Name", default="")

    tris: bpy.props.IntProperty(default=0)
    verts: bpy.props.IntProperty(default=0)

    material_count: bpy.props.IntProperty(default=0)
    material_node_count: bpy.props.IntProperty(default=0)

    modifier_count: bpy.props.IntProperty(default=0)


class CollectionCache(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Collection Name", default="")

    total_tris: bpy.props.IntProperty(default=0)
    total_verts: bpy.props.IntProperty(default=0)

    instance_count: bpy.props.IntProperty(default=0)  # all collection instances (recursive)


class NodeCache(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Node Name", default="")

    nodes_used: bpy.props.IntProperty(default=0)
