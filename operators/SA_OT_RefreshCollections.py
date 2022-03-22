import bpy
from ..model.CacheGroups import CollectionCache


def coll_iter(curr_coll):
    """
    Iterate through hierarchy of collections
    :param curr_coll: current collection
    :return: generator of collections
    """
    yield curr_coll
    for child in curr_coll.children:
        yield from coll_iter(child)


def find_coll_instancers(curr_coll):
    """
    Find all objects that instance collections
    :param curr_coll: current collection
    :return: generator of objects that instance collections
    """
    return (obj for obj in curr_coll.all_objects if obj.is_instancer and obj.instance_type == 'COLLECTION')


def find_instanced_colls(curr_coll):
    """
    Iterate over collections instanced by objects
    :param curr_coll: current collection
    :return: generator of collections that are instanced by objects
    """
    return (o.instance_collection for o in find_coll_instancers(curr_coll))


# example: find_instanced_colls(context.view_layer.layer_collection)
def find_instanced_objs_in_colls(curr_coll):
    """
    Iterate over objects that are in collections instanced by objects
    :param curr_coll: current collection
    :return: generator of objects in collections instanced by objects
    """
    objs_dict = {}
    for coll in find_instanced_colls(curr_coll):
        for obj in coll.all_objects:
            if obj not in objs_dict:
                objs_dict[obj] = True
                yield obj


class SA_OT_RefreshCollections(bpy.types.Operator):
    bl_idname = 'scene_analyzer.refresh_collections'
    bl_label = 'Refresh collections'
    bl_description = 'Refresh cache of collection stats'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        window_manager = context.window_manager
        root_collection = context.view_layer.layer_collection.collection
        window_manager.sa_collection_cache.clear()

        mesh_cache = {o.name: (o.tris, o.verts) for o in window_manager.sa_mesh_cache.values()}

        instanced_colls = [c.name for c in find_instanced_colls(root_collection)]

        for coll in coll_iter(root_collection):
            new_coll_data: CollectionCache = window_manager.sa_collection_cache.add()
            new_coll_data.name = coll.name
            for o in coll.objects:
                if o.name in mesh_cache:
                    tris, verts = mesh_cache[o.name]
                    new_coll_data.total_tris += tris
                    new_coll_data.total_verts += verts
            new_coll_data.instance_count = len([c for c in instanced_colls if c == coll.name])

        return {'FINISHED'}
