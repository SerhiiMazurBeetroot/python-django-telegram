from deep_translator import GoogleTranslator


def t(text):
    try:
        translated = GoogleTranslator(
            source="en",
            target="uk",
        ).translate(text)

        return translated
    except Exception as e:
        return f"Translation error: {str(e)}"
