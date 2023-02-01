from .. import register_all
from .. import unregister_all

from .SA_OT_RefreshAll import SA_OT_RefreshAll
from .SA_OT_RefreshMeshes import SA_OT_RefreshMeshes
from .SA_OT_RefreshCollections import SA_OT_RefreshCollections
from .SA_OT_RefreshNodes import SA_OT_RefreshNodes

_register_order = (SA_OT_RefreshMeshes, SA_OT_RefreshCollections, SA_OT_RefreshNodes, SA_OT_RefreshAll)


def register():
    register_all(_register_order)


def unregister():
    unregister_all(_register_order[::-1])
