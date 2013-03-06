# emacs-mode: -*- python-*-
import Live
from _Framework.SessionComponent import SessionComponent
from _Framework.CompoundComponent import CompoundComponent
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.MixerComponent import MixerComponent
from _Framework.ButtonElement import ButtonElement
from ConfigurableButtonElement import ConfigurableButtonElement
from SpecialSceneComponent import SpecialSceneComponent

class SpecialSessionComponent(SessionComponent):
    __module__ = __name__
    __doc__ = ' Special session subclass that handles ConfigurableButtons '

    def __init__(self, parent, num_tracks, num_scenes):
        SessionComponent.__init__(self, num_tracks, num_scenes)


        self._track_nav = False
        self._selected_scene = SpecialSceneComponent(self._num_tracks, self.tracks_to_use)
        self.on_selected_scene_changed()
        self.register_components(self._selected_scene)

    def _create_scene(self):
        return SpecialSceneComponent(num_slots=self._num_tracks, tracks_to_use_callback=self.tracks_to_use)

    def _bank_left_value(self, value):
        if (value == 127):
            self._track_nav = True
        else:
            self._track_nav = False

    def _bank_up_value(self, value):
        assert (value in range(1))
        assert (self._bank_up_button != None)
        if self._track_nav:
            if (value == 127):
                self.set_offsets(max(0, (self._track_offset - 1)), self._scene_offset)
            else:
                self.set_offsets((self._track_offset + 1), self._scene_offset)
        else:
            if (value == 127):
                self.set_offsets(self._track_offset, max(0, self._scene_offset - 1))
            else:
                self.set_offsets(self._track_offset, (self._scene_offset + 1))

    def _bank_down_value(self, value):
        pass
    def _bank_right_value(self, value):
        pass


# local variables:
# tab-width: 4
