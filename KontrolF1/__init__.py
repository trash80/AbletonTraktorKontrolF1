# emacs-mode: -*- python-*-
from KontrolF1 import KontrolF1

def create_instance(c_instance):
    """ Creates and returns the KontrolF1 script """
    return KontrolF1(c_instance)

from _Framework.Capabilities import *

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=8080, product_ids=[808], model_name='Traktor Kontrol F1'),
     PORTS_KEY: [inport(props=[NOTES_CC, REMOTE, SCRIPT]), outport(props=[NOTES_CC, REMOTE, SCRIPT])]}

# local variables:
# tab-width: 4
