
def adjust_capitalization(old_word, new_word):

    results = new_word

    if old_word.upper() == old_word:
        results = new_word.upper()
    else:
        if old_word.lower() == old_word:
            pass
        else:
            results = new_word[:1].upper() + new_word[1:]

    return results
