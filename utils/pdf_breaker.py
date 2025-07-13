import re

def break_long_words(text, max_len=50):
    def insert_spaces(match):
        word = match.group(0)
        # Break word into chunks of max_len with spaces
        return ' '.join([word[i:i+max_len] for i in range(0, len(word), max_len)])
    # Regex to find words longer than max_len without spaces
    return re.sub(r'\S{' + str(max_len+1) + r',}', insert_spaces, text)
