
from __future__ import with_statement
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from ConfigurableButtonElement import ConfigurableButtonElement
from SpecialSessionComponent import SpecialSessionComponent
from SpecialSceneComponent import SpecialSceneComponent
from SpecialClipSlotComponent import SpecialClipSlotComponent

SCENE_LAUNCH = (56,57,58,59)
STOP_LAUNCH = (60,61,62,63)
NAV_BUTTONS = (105,106,107,108)
WIDTH = 4
HEIGHT= 4
class KontrolF1(ControlSurface):
    __module__ = __name__
    __doc__ = " Script for Native Instruments Traktor Kontrol F1 Controller "

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)

        with self.component_guard():
            self._suppress_send_midi = True
            self._suppress_session_highlight = True
            self.log_message("KontrolF1 Started!")
            self._suggested_input_port = 'Traktor Kontrol F1'
            self._suggested_output_port = 'Traktor Kontrol F1'

            self._blink_state = False

            self._matrix = ButtonMatrixElement()
            for row in range(HEIGHT):
                button_row = [ ConfigurableButtonElement( True, MIDI_CC_TYPE, 2, ((row * HEIGHT) + column)) for column in range(WIDTH) ]
                self._matrix.add_row(tuple(button_row))

            self._nav_buttons  = [ ButtonElement( False, MIDI_NOTE_TYPE, 0, NAV_BUTTONS[0]),
                                   ButtonElement( False, MIDI_NOTE_TYPE, 0, NAV_BUTTONS[1]),
                                   ButtonElement( True, MIDI_NOTE_TYPE, 0, NAV_BUTTONS[2]),
                                   ButtonElement( True, MIDI_NOTE_TYPE, 0, NAV_BUTTONS[3])]
            self._scene_buttons = [ ConfigurableButtonElement( True, MIDI_CC_TYPE, 0, SCENE_LAUNCH[index]) for index in range(HEIGHT) ]
            
            self._stop_buttons = []
            for index in range(WIDTH):
                self._stop_buttons.append(ConfigurableButtonElement( True, MIDI_CC_TYPE, 0, STOP_LAUNCH[index]))
            
            self._session = SpecialSessionComponent(self, self._matrix.width(), self._matrix.height())
            

            self._all_buttons = []
            for button in (self._scene_buttons + self._nav_buttons + self._stop_buttons):
                self._all_buttons.append(button)

            for scene_index in range(self._matrix.height()):
                for track_index in range(self._matrix.width()):
                    self._all_buttons.append(self._matrix.get_button(track_index, scene_index))
            self._all_buttons = tuple(self._all_buttons)



            self._suppress_session_highlight = False
            self._suppress_send_midi = False
            self.set_highlighting_session_component(self.session_component())
            self.update()
            self.set_enabled(True)
            self.log_message("KontrolF1 Initialized!")
            #self._set_session_highlight(0,0,WIDTH,HEIGHT,True)

    def disconnect(self):
        self._suppress_send_midi = True

        self._session = None
        for button in self._all_buttons:
            button.set_on_off_values(127, 0)

        self._matrix = None
        self._stop_buttons = None
        self._scene_buttons = None
        self._nav_buttons = None

        ControlSurface.disconnect(self)
        self._suppress_send_midi = False

    def highlighting_session_component(self):
        " Return the session component showing the ring in Live session "
        return self.session_component()

    def update_display(self):
        tracks = self.song().visible_tracks
        number_tracks = len(tracks)

        if self._blink_state:
            self._blink_state = False
        else:
            self._blink_state = True

        for track in range(WIDTH):
            to = track + self._session._track_offset
            if (to < number_tracks):
                for y in range(HEIGHT):
                    ys = self._session._scene_offset+y
                    yx = (y*4)+track
                    slot = tracks[to].clip_slots[ys]
                    if (slot.controls_other_clips) or (slot.has_clip):
                        if slot.is_triggered:
                            if self._blink_state:
                                self._send_midi(tuple([178,yx,40]))
                            else:
                                self._send_midi(tuple([178,yx,127]))
                    elif slot.is_triggered:
                        if self._blink_state:
                            self._send_midi(tuple([178,yx,0]))
                        else:
                            self._send_midi(tuple([178,yx,60]))

               


    def session_component(self):
        return self._session

    def refresh_state(self):
        ControlSurface.refresh_state(self)

    def _send_midi(self, midi_bytes, optimized = None):
        sent_successfully = False
        if not self._suppress_send_midi:
            sent_successfully = ControlSurface._send_midi(self, midi_bytes, optimized=optimized)
        return sent_successfully

    def _update_hardware(self):
        pass

    def _send_challenge(self):
        pass

    def _config_value(self, value):
        assert (value in range(128))

    def _set_session_highlight(self, track_offset, scene_offset, width, height, include_return_tracks):
        ControlSurface._set_session_highlight(self, track_offset, scene_offset, width, height, include_return_tracks)

    #def _install_forwarding(self, control):
    #    result = ControlSurface._install_forwarding(self, control)
    #    return result

    def _translate_message(self, type, from_identifier, from_channel, to_identifier, to_channel):
        ControlSurface._translate_message(self, type, from_identifier, from_channel, to_identifier, to_channel)


    def on_enabled_changed(self):
        self.update()

    def update(self):
        
        self._session.set_allow_update(False)


        for scene_index in range(HEIGHT):
            scene = self._session.scene(scene_index)
            scene.set_launch_button(self._scene_buttons[scene_index])
            for track_index in range(WIDTH):
                scene.clip_slot(track_index).set_launch_button(self._matrix.get_button(track_index, scene_index))

        #self.log_message(str(tuple(self._stop_buttons)))
        self._session.set_stop_track_clip_buttons(tuple(self._stop_buttons))
        self._session.set_scene_bank_buttons(self._nav_buttons[0], self._nav_buttons[1])
        self._session.set_track_bank_buttons(self._nav_buttons[2], self._nav_buttons[3])
        self._session.set_allow_update(True)