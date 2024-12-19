from pythainlp.tokenize import word_tokenize
from pythainlp.spell import correct
import re

def th_tokenizer(text)-> str:

    # utf8_bytes = text.encode('utf-8')
    # decoded_string = utf8_bytes.decode('utf-8')

    # print("\ndecode test: ", decoded_string)
    
    tokenized_text = word_tokenize(text, keep_whitespace=True)
    
    test = []

    for i in  range(len(tokenized_text)):
        test.append(correct(tokenized_text[i]))
        
    print(test)


    print("\ntest: ", ' '.join(test))

    return ' '.join(tokenized_text)
