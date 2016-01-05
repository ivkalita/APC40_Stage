#Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/midi-remote-scripts/APC40/__init__.py
from _Framework.Capabilities import CONTROLLER_ID_KEY, PORTS_KEY, NOTES_CC, SCRIPT, REMOTE, controller_id, inport, outport
from APC40_Stage import APC40

def create_instance(c_instance):
    return APC40.APC40(c_instance)


def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=2536, product_ids=[115], model_name='Akai APC40'),
     PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[SCRIPT, REMOTE])]}