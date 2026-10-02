import arabic_reshaper

def text_to_persian(text) -> str:
    text_reshaped = arabic_reshaper.reshape(text)
    bidi_text = ""
    for i in text_reshaped:
        bidi_text = i + bidi_text
    return bidi_text