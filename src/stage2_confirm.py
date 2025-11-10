def is_yes(text: str) -> bool:
    text = text.lower().strip()

    YES_PATTERNS = [
        "yes", "yeah", "yea", "yep", "yup", "sure", "ok", "okay", "k",
        "do it", "go ahead", "please", "play", "start", "fine", "ig", "i guess",
        "why not", "sounds good", "bet", "ight", "do that", "alright", "go for it"
    ]

    return any(phrase in text for phrase in YES_PATTERNS)


def is_no(text: str) -> bool:
    text = text.lower().strip()

    NO_PATTERNS = [
        "no", "nah", "nope", "stop", "cancel", "don't", "dont", "not really",
        "please no", "i don't want", "leave it", "nvm", "nevermind", "idc", "i don't care",
        "no thanks", "i'm good", "im good", "not now", "stop it", "let's not"
    ]

    return any(phrase in text for phrase in NO_PATTERNS)
