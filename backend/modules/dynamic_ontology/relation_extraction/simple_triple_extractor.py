# simple_triple_extractor.py
from nltk.chunk import RegexpParser
from nltk.tree import Tree

from modules.pre_processing.sinhala_pos_tagger import SinhalaPOSTagger


# Define POS-based regular expressions for chunking
# These are simplified versions based on your guide.
# IMPORTANT: These are for demonstration and need fine-tuning for real accuracy!
NP_GRAMMAR = r"""
    NP: {<JJ>*<NUM>*<NN.*>+<POST>*}
        {<DET><NN.*>+<POST>*} 
        {<PRP.*>+<POST>*}
        NP: {<NNP>+<NNC>*}  # This is a valid rule, the comment is now correctly identified
        # Add more patterns to capture complex noun phrases
"""

VP_GRAMMAR = r"""
    VP: {<JCV>*<NCV>*<PCV>*<VFM>+}
        {<JCV>*<NCV>*<PCV>*<VP>+}
        {<JCV>*<NCV>*<PCV>*<VNF>+}
        {<JCV>*<NCV>*<PCV>*<VNN>+}
        {<NVB>+} # Sentence ending words that act like verbs
        # More general verb patterns
        {<VFM>+}
        {<VP>+}
        {<VNF>+}
        {<VNN>+}
"""

# Combine into a single grammar for RegexpParser
# NLTK processes rules in order.
CHUNK_GRAMMAR = f"{NP_GRAMMAR}\n{VP_GRAMMAR}"
CHUNK_PARSER = RegexpParser(CHUNK_GRAMMAR)

# Define boundary terms for Constraint 1
CONSTRAINT1_BOUNDARIES = {"බව", "බවයි"}


def _apply_constraint1_simple(chunk_tree: Tree) -> list:
    """
    (Helper) Applies a simplified Syntactic Constraint 1 (based on 'බව'/'බවයි' POST boundary).
    Assumes LHS is Object-like content, RHS contains Subject & Verb.
    Returns a list of (Subject, Verb, Object) tuples.
    """
    triples = []
    words = list(chunk_tree.leaves())  # Get all (word, tag) tuples

    boundary_index = -1
    for i, (word, tag) in enumerate(words):
        if word in CONSTRAINT1_BOUNDARIES and tag == "POST":
            boundary_index = i
            break

    if boundary_index != -1:
        # Left-hand side is the content of the reported event (conceptual Object)
        left_side_words = words[:boundary_index]
        # Right-hand side is the main reporting S + V
        right_side_words = words[boundary_index + 1 :]

        # Re-parse for chunks on each side
        left_chunk_tree = CHUNK_PARSER.parse(left_side_words)
        right_chunk_tree = CHUNK_PARSER.parse(right_side_words)

        # Extract Object from LHS
        # The paper implies this could be a complex clause.
        # For simple function, take the full string content of LHS.
        obj_content = " ".join(leaf[0] for leaf in left_side_words).strip()

        # Extract Subject and Verb from RHS
        # Simple approach: find first NP as Subject, first VP as Verb
        sub_phrases = []
        verb_phrases = []

        for subtree in right_chunk_tree.subtrees():
            if subtree.label() == "NP":
                sub_phrases.append(" ".join(leaf[0] for leaf in subtree.leaves()))
            elif subtree.label() == "VP":
                verb_phrases.append(" ".join(leaf[0] for leaf in subtree.leaves()))

        subject = sub_phrases[0] if sub_phrases else "N/A_Subject"
        verb = verb_phrases[0] if verb_phrases else "N/A_Verb"

        triples.append((subject, verb, obj_content))

    return triples


def _apply_constraint2_simple(chunk_tree: Tree) -> list:
    """
    (Helper) Applies a simplified Syntactic Constraint 2 (for sentences without boundaries).
    Heuristic: last VP is main verb. If multiple NPs, first is Subject, second is Object.
    """
    triples = []

    noun_phrases_text = []
    verb_phrases_text = []

    for subtree in chunk_tree.subtrees():
        if subtree.label() == "NP":
            noun_phrases_text.append(" ".join(leaf[0] for leaf in subtree.leaves()))
        elif subtree.label() == "VP":
            verb_phrases_text.append(" ".join(leaf[0] for leaf in subtree.leaves()))

    if verb_phrases_text:
        main_verb = verb_phrases_text[-1]  # Take the last VP as the main verb

        subject = "N/A_Subject"
        obj = "N/A_Object"

        if len(noun_phrases_text) >= 1:
            subject = noun_phrases_text[
                0
            ]  # First NP is often the subject in SOV context
        if len(noun_phrases_text) >= 2:
            obj = noun_phrases_text[1]  # Second NP is often the object

        triples.append((subject, main_verb, obj))

    return triples


def extract_triple_extraction(text: str, pos_tagger_instance: SinhalaPOSTagger) -> dict:
    """
    Extracts basic Subject-Verb-Object (SOV) triples from a single Sinhala sentence.
    Applies a simplified version of Constraint 1 if 'බව'/'බවයි' is present,
    otherwise applies a simplified Constraint 2.

    Args:
        text (str): The input Sinhala sentence. It should be minimally preprocessed
                    (URLs/emojis removed, but punctuation, numbers, non-Sinhala words,
                    original forms kept, and words space-separated).
        pos_tagger_instance (SinhalaPOSTagger): An initialized instance of your
                                                SinhalaPOSTagger for POS tagging.

    Returns:
        dict: A dictionary containing:
              - 'original_text': The input text.
              - 'tagged_words': The POS-tagged version of the text.
              - 'chunk_tree': The NLTK parse tree after chunking (as a string).
              - 'extracted_triples': A list of (subject, verb, object) tuples.
    """
    if not text:
        return {
            "original_text": text,
            "tagged_words": [],
            "chunk_tree": "",
            "extracted_triples": [],
        }

    # 1. POS Tagging
    # The POS tagger expects space-separated tokens.
    tagged_words = pos_tagger_instance.pos_tagging(text)

    # If no words were tagged or all are UNK, might not be able to proceed
    if not tagged_words:
        return {
            "original_text": text,
            "tagged_words": tagged_words,
            "chunk_tree": "",
            "extracted_triples": [],
        }

    # 2. Chunking (Partial Parsing)
    chunk_tree = CHUNK_PARSER.parse(tagged_words)

    # 3. Apply Syntactic Constraints for Triple Extraction
    triples = _apply_constraint1_simple(chunk_tree)

    if not triples:
        # If Constraint 1 didn't yield triples, try Constraint 2
        triples = _apply_constraint2_simple(chunk_tree)

    return {
        "original_text": text,
        "tagged_words": tagged_words,
        "chunk_tree": str(chunk_tree),  # Convert tree to string for easier viewing
        "extracted_triples": triples,
    }


# --- Example Usage ---
if __name__ == "__main__":
    # Initialize the POS tagger ONCE for demonstration
    # Make sure 'postagger.txt' is in the same directory for SinhalaPOSTagger
    tagger = SinhalaPOSTagger()

    # Sample sentences (same as NER enhanced extractor)
    import json
    import os

    os.makedirs("logs", exist_ok=True)

    sample_texts = [
        "ඉන්දීය ජනප්‍රිය දෙමළ සහ තෙළිඟු නළු ශ්‍රීකාන්ත් අත්අඩංගුවට ගෙන තිබෙන බව විදෙස් මාධ්‍ය වාර්තා කරනවා",
        "ජනාධිපති රනිල් වික්‍රමසිංහ ජපානයට ගියා",
        "ලංකාදීප COVID-19 වාර්තා පළ කළා",
        "මිනිසා වේගයෙන් දුවයි",
    ]

    results = []
    for text in sample_texts:
        result = extract_triple_extraction(text, tagger)
        results.append({"sentence": text, "result": result})

    with open("logs/simple_triple_extractor_output.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("Results saved to logs/simple_triple_extractor_output.json.")
