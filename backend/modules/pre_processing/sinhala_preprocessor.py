import re
import emoji
import os  # For file path operations


class SinhalaPreprocessor:
    """
    A class for preprocessing Sinhala text with configurable options.
    Loads stop words and a stemming dictionary from default locations
    (same directory as the script) upon initialization.

    Individual preprocessing steps are also exposed as public methods for modular use.
    """

    def __init__(self):
        """
        Initializes the SinhalaPreprocessor, loading necessary resources
        from default file locations (StopWords.txt and stem_dictionary.txt
        expected in the same directory as this script).
        """
        self.stopwords = self._load_stopwords()
        self.stem_dictionary = self._load_stem_dictionary()

        print("--- SinhalaPreprocessor Initialized ---")
        print(f"Stop words loaded: {len(self.stopwords)} words")
        print(f"Stem dictionary loaded: {len(self.stem_dictionary)} entries")
        print("-" * 30)

    # --- Private Helper Methods for Resource Loading ---

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

    def _load_stopwords(self) -> set:
        """
        (Private Helper) Loads Sinhala stop words from 'stopwords.txt'.
        """
        filepath = self._get_resource_path("stopwords.txt")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return {line.strip() for line in f if line.strip()}
        except FileNotFoundError:
            print(
                f"Error: Stop words file not found at {filepath}. Returning empty set."
            )
            return set()
        except Exception as e:
            print(
                f"Error loading stop words from {filepath}: {e}. Returning empty set."
            )
            return set()

    def _load_stem_dictionary(self) -> dict:
        """
        (Private Helper) Loads a Sinhala stemming dictionary from 'stem_dictionary.txt'.
        """
        filepath = self._get_resource_path("stem_dictionary.txt")
        stem_dict = {}
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("\t")
                    if len(parts) == 2:
                        stem_dict[parts[0]] = parts[1]
            return stem_dict
        except FileNotFoundError:
            print(
                f"Error: Stem dictionary file not found at {filepath}. Returning empty dictionary."
            )
            return {}
        except Exception as e:
            print(
                f"Error loading stem dictionary from {filepath}: {e}. Returning empty dictionary."
            )
            return {}

    # --- Public Helper Methods for Individual Preprocessing Steps ---

    def remove_urls(self, text: str) -> str:
        """Removes URLs from the text."""
        return re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)

    def remove_emojis(self, text: str) -> str:
        """Removes emojis from the text."""
        text = emoji.demojize(text)
        return re.sub(r":\S+:", "", text)

    def remove_non_sinhala_and_handle_numbers(
        self, text: str, keep_numbers: bool = True
    ) -> str:
        """
        Removes non-Sinhala characters.
        If `keep_numbers` is True, digits (0-9) are preserved.
        """
        chars_to_keep = r"\u0D80-\u0DFF"  # Sinhala Unicode range
        if keep_numbers:
            chars_to_keep += r"\u0030-\u0039"  # Add ASCII digits 0-9

        # Match anything NOT in the chars_to_keep set AND NOT a whitespace
        regex_pattern = r"[^" + chars_to_keep + r"\s]+"
        return re.sub(regex_pattern, "", text)

    def remove_punctuation(self, text: str) -> str:
        """Removes common punctuation marks."""
        return re.sub(r"[.,;!?-@#$%^&*()_+={}\[\]|\\:\"'<>/~`‘’“”]", "", text)

    def normalize_whitespace(self, text: str) -> str:
        """Replaces multiple whitespaces with single spaces and strips leading/trailing space."""
        return re.sub(r"\s+", " ", text).strip()

    def remove_stopwords(self, text: str) -> str:
        """
        Removes stop words from the text. Assumes text is space-tokenized.
        Will warn if stopwords are not loaded.
        """
        if not self.stopwords:
            print(
                "Warning: Stop words list is empty or not loaded. Skipping stop word removal."
            )
            return text
        words = text.split()
        filtered_words = [word for word in words if word not in self.stopwords]
        return " ".join(filtered_words)

    def apply_stemming(self, text: str) -> str:
        """
        Applies dictionary-based stemming to the text. Assumes text is space-tokenized.
        Will warn if stem dictionary is not loaded.
        """
        if not self.stem_dictionary:
            print("Warning: Stem dictionary is empty or not loaded. Skipping stemming.")
            return text
        words = text.split()
        stemmed_words = [self.stem_dictionary.get(word, word) for word in words]
        return " ".join(stemmed_words)

    # --- Main Composite Preprocessing Method ---

    def preprocess_text(
        self,
        text: str,
        remove_emojis: bool = True,
        remove_urls: bool = True,
        remove_non_sinhala_chars: bool = True,
        remove_numbers: bool = False,  # Default to False (keep numbers)
        remove_punctuation: bool = True,
        remove_stopwords: bool = True,
        apply_stemming: bool = False,
    ) -> str:
        """
        Applies a composite preprocessing pipeline to Sinhala text with configurable options.
        This method calls the individual public helper methods in a predefined order.

        Args:
            text (str): The input Sinhala text.
            remove_emojis (bool): Whether to remove emojis. Defaults to True.
            remove_urls (bool): Whether to remove URLs. Defaults to True.
            remove_non_sinhala_chars (bool): Whether to remove characters outside the Sinhala Unicode range.
                                           If False, and remove_numbers is True, only numbers will be removed.
                                           Defaults to True.
            remove_numbers (bool): Whether to remove digits (0-9). Defaults to False.
            remove_punctuation (bool): Whether to remove common punctuation marks. Defaults to True.
            remove_stopwords (bool): Whether to remove stop words. Defaults to True.
            apply_stemming (bool): Whether to apply dictionary-based stemming. Defaults to True.

        Returns:
            str: The preprocessed Sinhala text.
        """

        processed_text = text

        if remove_urls:
            processed_text = self.remove_urls(processed_text)
        if remove_emojis:
            processed_text = self.remove_emojis(processed_text)

        # Order matters here for `remove_non_sinhala_chars` and `remove_numbers`
        if remove_non_sinhala_chars:
            # If `remove_non_sinhala_chars` is True, it dictates whether numbers are kept/removed.
            processed_text = self.remove_non_sinhala_and_handle_numbers(
                processed_text, keep_numbers=not remove_numbers
            )
        elif remove_numbers:
            # If `remove_non_sinhala_chars` is False, but `remove_numbers` is True,
            # we explicitly remove *only* numbers without affecting other non-Sinhala chars.
            processed_text = re.sub(r"[\u0030-\u0039]+", "", processed_text)

        if remove_punctuation:
            processed_text = self.remove_punctuation(processed_text)

        # Normalize whitespace early for consistent tokenization later
        processed_text = self.normalize_whitespace(processed_text)

        # Note: Stop word removal and stemming operate on tokenized (space-separated) words.
        # This function implicitly tokenizes by splitting on spaces.
        if remove_stopwords:
            processed_text = self.remove_stopwords(processed_text)

        if apply_stemming:
            processed_text = self.apply_stemming(processed_text)

        return processed_text


# --- Example Usage ---
if __name__ == "__main__":
    # Create an instance of the preprocessor. Resources are loaded automatically.
    preprocessor = SinhalaPreprocessor()

    sample_text = "ගුවන්තොටුපළ ඉදිරිපිට ගුටිබැට https://example.com ✈️ 2024 අයවැය 5% ක වැඩිවීමක්. අද හොඳ දවසක්. එය විශිෂ්ටයි! 😊 Some English words here. #news"

    print(f"\nOriginal Text:\n{sample_text}\n")

    # --- Using the composite preprocess_text method (same as before) ---
    print("--- 1. Using composite preprocess_text (default config) ---")
    processed_composite = preprocessor.preprocess_text(sample_text)
    print(f"Composite Processed:\n{processed_composite}\n")

    # --- Using individual methods for a custom pipeline ---
    print("--- 2. Building a custom pipeline with individual methods ---")
    custom_processed_text = sample_text

    # Step 1: Remove URLs
    custom_processed_text = preprocessor.remove_urls(custom_processed_text)
    print(
        f"After URL removal: {custom_processed_text[:80]}...\n"
    )  # Truncate for display

    # Step 2: Remove Emojis
    custom_processed_text = preprocessor.remove_emojis(custom_processed_text)
    print(f"After Emoji removal: {custom_processed_text[:80]}...\n")

    # Step 3: Remove Punctuation
    custom_processed_text = preprocessor.remove_punctuation(custom_processed_text)
    print(f"After Punctuation removal: {custom_processed_text[:80]}...\n")

    # Step 4: Remove non-Sinhala characters but KEEP numbers
    custom_processed_text = preprocessor.remove_non_sinhala_and_handle_numbers(
        custom_processed_text, keep_numbers=True
    )
    print(f"After Non-Sinhala/Number handling: {custom_processed_text[:80]}...\n")

    # Step 5: Normalize whitespace (important before tokenization)
    custom_processed_text = preprocessor.normalize_whitespace(custom_processed_text)
    print(f"After Whitespace Normalization: '{custom_processed_text}'\n")

    # Step 6: Remove Stop Words
    custom_processed_text = preprocessor.remove_stopwords(custom_processed_text)
    print(f"After Stop Words removal: '{custom_processed_text}'\n")

    # Step 7: Apply Stemming
    custom_processed_text = preprocessor.apply_stemming(custom_processed_text)
    print(f"After Stemming: '{custom_processed_text}'\n")

    print("-" * 50)
    print("\nNotice how you can control each step independently now!")

    # --- Example: Just removing URLs ---
    print("\n--- 3. Just removing URLs ---")
    just_urls_removed = preprocessor.remove_urls(sample_text)
    print(f"Original: '{sample_text}'")
    print(f"Just URLs removed: '{just_urls_removed}'\n")

    # --- Example: Just stemming ---
    print("\n--- 4. Just Stemming a pre-tokenized string ---")
    text_to_stem = "ගුවන්තොටුපළ ඉදිරිපිට ගුටිබැට"
    stemmed_only = preprocessor.apply_stemming(text_to_stem)
    print(f"Original: '{text_to_stem}'")
    print(f"Just Stemmed: '{stemmed_only}'\n")
