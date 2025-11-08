def is_yes(text):
    text = text.lower().strip()
    return text in ["yes","yeah","yup","sure","go ahead","do it","ok","please","play","start","proceed"]

def is_no(text):
    text = text.lower().strip()
    return text in ["no","nah","nope","stop","cancel","not really"]
