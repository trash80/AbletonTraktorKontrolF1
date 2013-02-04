# --== Decompile ==--

import Live
from _Framework.CompoundComponent import CompoundComponent
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SceneComponent import SceneComponent
from _Framework.ButtonElement import ButtonElement
from SpecialClipSlotComponent import SpecialClipSlotComponent

class SpecialSceneComponent(SceneComponent):
    __module__ = __name__
    __doc__ = ' Class representing a scene in Live '
    def __init__(self, num_slots, tracks_to_use_callback):
        SceneComponent.__init__(self, num_slots, tracks_to_use_callback)
        return None

    def _create_clip_slot(self):
        return SpecialClipSlotComponent()
    