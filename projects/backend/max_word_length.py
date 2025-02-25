import json

from tqdm import tqdm
from typing import List, Tuple


def get_max_word_length(documents: List[dict]) -> Tuple[int, str]:
    max_word_length = 0
    longest_word = ""
    for document in tqdm(documents, total=len(documents), desc="Calculating max word length"):
        for word in document["title"].split():
            max_word_length = max(max_word_length, len(word))
            longest_word = max(longest_word, word, key=len)

        for word in document["explanation"].split():
            max_word_length = max(max_word_length, len(word))
            longest_word = max(longest_word, word, key=len)
    return max_word_length, longest_word


if __name__ == "__main__":
    with open("../../data/apod.json") as file:
        documents = json.load(file)
    
    max_word_length, longest_word = get_max_word_length(documents=documents)
    print(f"Max word length: {max_word_length}")
    print(f"Longest word: {longest_word}")
