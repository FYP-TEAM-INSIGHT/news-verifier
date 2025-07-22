"""
Sinhala POS Tagger
Loads POS tags from a resource file and provides tagging for input text.
"""

from typing import List, Tuple, Dict, Optional
import os


class SinhalaPOSTagger:
    def __init__(
        self,
    ):
        self.pos_dict = self._load_pos_tags()

    def _get_resource_path(self, filename: str) -> str:
        """
        Helper to get the full path to a resource file located in backend/data/models.
        """
        # Get the backend directory
        backend_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        models_dir = os.path.join(backend_dir, "data", "models")
        return os.path.join(models_dir, filename)

    def _load_pos_tags(self) -> Dict[str, str]:
        filePath = self._get_resource_path("sinhala_pos.txt")

        pos_dict = {}
        with open(filePath, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):  # skip empty/comments
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    word = parts[0]
                    tag = parts[1]
                    pos_dict[word] = tag
        return pos_dict

    def tag(self, tokens: List[str]) -> List[Tuple[str, Optional[str]]]:
        """
        Tags a list of tokens with their POS tags. Returns (token, tag) tuples.
        If a token is not found, tag is None.
        """
        return [(token, self.pos_dict.get(token)) for token in tokens]

    def tag_sentence(
        self, sentence: str, delimiter: str = " "
    ) -> List[Tuple[str, Optional[str]]]:
        tokens = sentence.strip().split(delimiter)
        return self.tag(tokens)

    def pos_tagging(self, text: str) -> list:
        """
        Performs POS tagging on the given Sinhala text.

        Args:
            text (str): The input Sinhala text. It is assumed that the text
                        is already preprocessed (e.g., cleaned, tokenized into
                        space-separated words).

        Returns:
            list: A list of tuples, where each tuple is (word, tag).
                  If a word is not found in the dictionary, its tag will be 'UNK' (Unknown).
                  If a word has multiple tags in the dictionary, only the first one found
                  is returned.
        """
        if not text:
            return []

        # Assuming text is already tokenized (space-separated words)
        words = text.split()
        tagged_words = []

        for word in words:
            # Look up the word in the loaded dictionary

            # If multiple tags exist, pick the first one.
            # You might implement more sophisticated disambiguation here if needed.
            chosen_tag = self.pos_dict.get(word, "UNK")

            tagged_words.append((word, chosen_tag))

        return tagged_words


if __name__ == "__main__":
    # Initialize the POS tagger (loads the file once)
    tagger = SinhalaPOSTagger()

    # Sample texts for tagging
    text1 = "අද දින මහ වැසි."  # Example from previous scenario
    text2 = "ප්‍රියන්ත අමරසිංහ ගෙදර ගියා."
    text3 = "ඔයාගේ කැමතිම චිත්‍රපටිය කුමක්ද."  # "චිත්‍රපටිය" not in dummy dict
    text4 = "වන වාණිජ හා පාරිභෝගික කටයුතු."
    text5 = "හතරයි ගෙන යෑම බැලීමට."

    text = "ඉන්දීය ජනප්‍රිය දෙමළ සහ තෙළිඟු නළු ශ්‍රීකාන්ත් අත්අඩංගුවට ගෙන තිබෙන බව විදෙස් මාධ්‍ය වාර්තා කරනවා"

    print("\n--- POS Tagging Examples ---")

    print(f"\nText: '{text}'")
    print(
        f"Tags: {tagger.pos_tagging(text)}"
    )  #  Tags: [('අද', 'NNC'), ('දින', 'NNC'), ('මහ', 'JJ'), ('වැසි.', 'UNK')]

    #  Tags: [('ඉන්දීය', 'NNP'), ('ජනප්\u200dරිය', 'JJ'), ('දෙමළ', 'NNP'), ('සහ', 'CC'), ('තෙළිඟු', 'NNP'), ('නළු', 'NNC'), ('ශ්\u200dරීකා        ාන්ත්', 'UNK'), ('අත්අඩංගුවට', 'NNC'), ('ගෙන', 'VNF'), ('තිබෙන', 'VP'), ('බව', 'POST'), ('විදෙස්', 'JJ'), ('මාධ්\u200dය', 'JJ'), ('ව       වාර්තා', 'NNC'), ('කරනවා', 'VFM')]

    # Actual ResultTags: [('ඉන්දීය', 'N'), ('ජනප්\u200dරිය', 'J'), ('දෙමළ', 'N'), ('සහ', 'C'), ('තෙළිඟු', 'J'), ('නළු', 'J'), ('ශ්\u200dරීකාන්ත්', 'UNK'), ('අත්අඩංගුවට', 'N'), ('ගෙන', 'ය'), ('තිබෙන', 'V')             ), ('බව', 'P'), ('විදෙස්', 'J'), ('මාධ්\u200dය', 'N'), ('වාර්තා', 'N'), ('කරනවා', 'V')]
