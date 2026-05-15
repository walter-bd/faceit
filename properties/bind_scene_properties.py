# Copyright (C) 2025 wben
# Modified to guard property deletions in unregister

from bpy.props import (BoolProperty)
from bpy.types import Scene


def register():

    Scene.faceit_weights_restorable = BoolProperty(
        default=False,
    )
    Scene.faceit_expressions_restorable = BoolProperty(
        default=False,
    )
    Scene.faceit_corrective_sk_restorable = BoolProperty(
        default=False,
    )


def unregister():
    if hasattr(Scene, 'faceit_weights_restorable'):

        del Scene.faceit_weights_restorable
    if hasattr(Scene, 'faceit_expressions_restorable'):

        del Scene.faceit_expressions_restorable
    if hasattr(Scene, 'faceit_corrective_sk_restorable'):

        del Scene.faceit_corrective_sk_restorable
