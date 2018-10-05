import json
import os
import pytest
import logging
from indic_transliteration import sanscript

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(filename)s:%(lineno)d %(message)s"
)


TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'transliterationTests.json')

test_data = {}
with open(TEST_DATA_PATH) as test_data_file:
    # noinspection PyRedeclaration
    test_data = json.loads(test_data_file.read())
logging.info(test_data["tests"])


SCRIPT_NAME_MAP= {
    "hk_sanscript": sanscript.HK
}


@pytest.mark.parametrize("test_conversions", test_data["tests"])
def test_to_devanagari(test_conversions):
    logging.debug(str(test_conversions))
    dev_string = test_conversions["dev"]
    for (script, text) in test_conversions.items():
        if script in SCRIPT_NAME_MAP.keys():
            script = SCRIPT_NAME_MAP[script]
        if script == "dev" or (script not in sanscript.SCHEMES.keys()):
            logging.debug("Skipping over script - " + script)
            continue
        assert dev_string == sanscript.transliterate(text, script, sanscript.DEVANAGARI), "Failed to convert " + script + " to devanAgarI: got " + sanscript.transliterate(text, script, sanscript.DEVANAGARI) + " instead of " + dev_string


def test_optitrans_to_itrans():
    assert sanscript.transliterate("shankara", sanscript.OPTITRANS, sanscript.ITRANS) == "sha~Nkara"
    assert sanscript.transliterate("manjIra", sanscript.OPTITRANS, sanscript.ITRANS) == "ma~njIra"
    assert sanscript.transliterate("praBA", sanscript.OPTITRANS, sanscript.ITRANS) == "prabhA"
    assert sanscript.transliterate("pRRS", sanscript.OPTITRANS, sanscript.ITRANS) == "pRRISh"
    assert sanscript.transliterate("pRcCa", sanscript.OPTITRANS, sanscript.ITRANS) == "pRRichCha"
    assert sanscript.transliterate("R", sanscript.OPTITRANS, sanscript.ITRANS) == "RRi"
    assert sanscript.transliterate("Rc", sanscript.OPTITRANS, sanscript.ITRANS) == "RRich"

def test_itrans_to_optitrans():
    assert sanscript.transliterate("sha~Nkara", sanscript.ITRANS, sanscript.OPTITRANS) == "shankara"
    assert sanscript.transliterate("ma~njIra", sanscript.ITRANS, sanscript.OPTITRANS) == "manjIra"
