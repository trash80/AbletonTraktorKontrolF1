
import Live
from _Framework.ButtonElement import *
class ConfigurableButtonElement(ButtonElement):
    __module__ = __name__
    __doc__ = ' Special button class that can be configured with custom on- and off-values '

    def __init__(self, is_momentary, msg_type, channel, identifier):
        ButtonElement.__init__(self, is_momentary, msg_type, channel, identifier, optimized_send_midi=False)
        self.identifier = identifier
        self.msg_type   = msg_type
        self.channel    = channel
        self._on_value = 127
        self._off_value = 0
        self._color = [0,0,0]
        self._is_notifying = False
        self._force_next_value = False
        self._pending_listeners = []
        self._color_cache= [-1,-1,-1]


    def set_on_off_values(self, on_value, off_value):
        assert (on_value in range(128))
        assert (off_value in range(128))
        self.clear_send_cache()
        self._on_value = on_value
        self._off_value = off_value



    def set_force_next_value(self):
        self._force_next_value = True

    def turn_on(self):
        self.send_value(self._on_value)



    def turn_off(self):
        self.send_value(self._off_value)



    def reset(self):
        self.send_value(4)

    def begin_undo_step(self):
        pass


    def add_value_listener(self, callback, identify_sender = False):
        if (not self._is_notifying):
            ButtonElement.add_value_listener(self, callback, identify_sender)
        else:
            self._pending_listeners.append((callback,
             identify_sender))

    def receive_value(self, value):
        self._is_notifying = True
        ButtonElement.receive_value(self, value)
        self._is_notifying = False
        for listener in self._pending_listeners:
            self.add_value_listener(listener[0], listener[1])

        self._pending_listeners = []


    def send_value(self, value, force = False):
        if isinstance(value, int):
            ButtonElement.send_value(self, value, (force or self._force_next_value))
        else:
            for c in range(3):
                self._send_midi(tuple([176+c,self.identifier,value[c]]))
        self._force_next_value = False

    def install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback):
        ButtonElement.install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback)
