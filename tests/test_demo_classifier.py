from register import Language, PronounRegisterClassifier, Register


def test_bengali_pronoun_registers():
    clf = PronounRegisterClassifier(Language.BENGALI)
    assert clf.classify("আপনি কেমন আছেন?").register is Register.FORMAL
    assert clf.classify("তুমি কোথায় যাচ্ছ?").register is Register.FAMILIAR
    assert clf.classify("তুই কী করছিস?").register is Register.INTIMATE


def test_hindi_pronoun_registers():
    clf = PronounRegisterClassifier(Language.HINDI)
    assert clf.classify("आप कैसे हैं?").register is Register.FORMAL
    assert clf.classify("तुम कहाँ जा रहे हो?").register is Register.FAMILIAR
    assert clf.classify("तू क्या कर रहा है?").register is Register.INTIMATE


def test_neutral_when_no_pronoun():
    clf = PronounRegisterClassifier(Language.HINDI)
    assert clf.classify("आज बारिश होगी।").register is Register.NEUTRAL


def test_mixed_when_two_registers():
    clf = PronounRegisterClassifier(Language.BENGALI)
    label = clf.classify("আপনি আর তুই একসাথে")
    assert label.register is Register.MIXED
    assert len(label.cues) >= 2


def test_confidence_and_cues_populated():
    clf = PronounRegisterClassifier(Language.HINDI)
    label = clf.classify("आप कैसे हैं?")
    assert label.confidence == 1.0
    assert label.is_marked()
    assert label.cues[0].surface == "आप"
