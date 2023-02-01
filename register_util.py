import bpy


def register_all(classes: tuple, window_manager_props: tuple = None):
    """Registers all provided classes and window manager properties.

    :param classes: tuple of Python classes
    :param window_manager_props: tuple of tuples, each nested tuple with its first element being a ``str`` name of the property, and a ``bpy.props`` property type as the second element.
    """
    for cls in classes:
        bpy.utils.register_class(cls)

    if window_manager_props is not None:
        window_manager = bpy.types.WindowManager
        for name, prop in window_manager_props:
            setattr(window_manager, name, prop)


def unregister_all(classes: tuple):
    """Unregisters all provided classes and window manager properties.

    :param classes: tuple of Python classes
    """
    for cls in classes:
        bpy.utils.unregister_class(cls)
