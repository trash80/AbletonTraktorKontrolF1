
import Live
from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.ButtonElement import ButtonElement
class SpecialClipSlotComponent(ClipSlotComponent):
    __doc__ = ' Class representing a ClipSlot within Live '
    
    def __init__(self):
        ClipSlotComponent.__init__(self)
        self.color = [-1,-1,-1]
        return None

    def update(self): #needs to be re-checked...
        self._has_fired_slot = False
        button = self._launch_button_value.subject
        if self._allow_updates:
            if (self.is_enabled() and button != None):
                value_to_send = [0,0,0]
                if (self._clip_slot != None):
                    if self.has_clip():
                        self.color = self.to_hsv(self._clip_slot.clip.color)
                        value_to_send = [self.color[0],self.color[1],30]
                        if self._clip_slot.clip.is_triggered:
                            if self._clip_slot.clip.will_record_on_start:
                                value_to_send = [0,127,30]
                            else:
                                value_to_send = [self.color[0],self.color[1],30]
                        elif self._clip_slot.clip.is_playing:
                            if self._clip_slot.clip.is_recording:
                                value_to_send = [0,127,127]
                            else:
                                value_to_send = [self.color[0],self.color[1],127]
                    elif self._clip_slot.is_triggered:
                        if self._clip_slot.will_record_on_start:
                            value_to_send = [0,127,30]
                        elif self._clip_slot.controls_other_clips:
                            value_to_send = [84, 60, 30]
                    elif self._clip_slot.is_playing:
                        if self._clip_slot.is_recording:
                            value_to_send = [0,127,127]
                        elif self._clip_slot.controls_other_clips:
                            value_to_send = [84, 40, 127]
                        #else:
                        #    value_to_send = [self.color[0],self.color[1],120]
                    elif self._clip_slot.controls_other_clips:
                        value_to_send = [84, 50, 30]
                button.send_value(value_to_send)
        else:
            self._update_requests += 1
        return None

    def to_hsv(self, rgb, inv = 0):
        b = rgb & 255
        g = (rgb >> 8) & 255
        r = (rgb >> 16) & 255
        r, g, b = r/255.0, g/255.0, b/255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx-mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g-b)/df) + 360) % 360
        elif mx == g:
            h = (60 * ((b-r)/df) + 120) % 360
        elif mx == b:
            h = (60 * ((r-g)/df) + 240) % 360
        if mx == 0:
            s = 0
        else:
            s = df/mx
        v = mx

        h = (int) (h/3)
        s = (int) (s*127)
        v = (int) (v*127)
        return h, s, v


