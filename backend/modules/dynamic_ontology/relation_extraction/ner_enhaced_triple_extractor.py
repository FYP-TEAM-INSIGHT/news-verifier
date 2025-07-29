# ner_enhanced_triple_extractor.py

import nltk
from nltk.chunk import RegexpParser
from nltk.tree import Tree

import requests
from modules.pre_processing.sinhala_pos_tagger import SinhalaPOSTagger


# NP_GRAMMAR_ENHANCED = r"""
#     NP: {<JJ>*<NUM>*<NNP_PERSON>+<POST>*}   # Prioritize NER-identified PERSON names
#         {<JJ>*<NUM>*<NNP_ORG>+<POST>*}     # Prioritize NER-identified ORG names
#         {<JJ>*<NUM>*<NNP_LOC>+<POST>*}     # Prioritize NER-identified LOC names
#         {<JJ>*<NUM>*<NNP_EVENT>+<POST>*}   # For 'EVENT' type
#         {<JJ>*<NUM>*<NNP>+<POST>*}         # General proper nouns
#         {<DET><JJ>*<NUM>*<NN.*>+<POST>*}   # Determiners with modifiers and common nouns
#         {<PRP.*>+<POST>*}                  # Pronouns
#         {<NN.*>+<POST>*}                   # Sequence of common nouns
#         # Add more rules as per your data patterns
# """

# VP_GRAMMAR_ENHANCED = r"""
#     VP: {<JCV>*<NCV>*<PCV>*<VFM>+} # Compound verbs ending in VFM
#         {<JCV>*<NCV>*<PCV>*<VP>+}  # Compound verbs ending in VP
#         {<JCV>*<NCV>*<PCV>*<VNF>+} # Compound verbs ending in VNF
#         {<JCV>*<NCV>*<PCV>*<VNN>+} # Compound verbs ending in VNN
#         {<NVB>+}                   # Sentence ending words
#         {<VFM>+}
#         {<VP>+}
#         {<VNF>+}
#         {<VNN>+}
#         # Add more rules for other verb forms/compounds if needed
# """

# NP_GRAMMAR_ENHANCED (Updated in ner_enhanced_triple_extractor.py)

NP_GRAMMAR_ENHANCED = r"""
    # 1. High-Priority NER-Enhanced Proper Nouns (most specific names and entities)
    #    Captures a sequence of NNP_ENTITY_TYPEs, optionally preceded by modifiers.
    #    Priority for multi-word names and titles/roles preceding them.
    NP: {<JJ|NNJ|NUM|NNC>*<NNP_PERSON>+<POST>*}   # e.g., 'ජනාධිපති/NNC රනිල්/NNP_PERON වික්‍රමසිංහ/NNP_PERON'
    NP: {<JJ|NNJ|NUM|NNC>*<NNP_ORG>+<POST>*}      # e.g., 'හමාස්/NNP_ORGANIZATION'
    NP: {<JJ|NNJ|NUM|NNC>*<NNP_LOC>+<POST>*}      # e.g., 'ගාසා/NNP_LOCATION තීරයේ/NNC_LOCATION' (if NNC_LOC matches)
    NP: {<JJ|NNJ|NUM|NNC>*<NNP_EVENT>+<POST>*}    # e.g., 'COVID-19/NNP_EVENT'
    
    # 2. General Proper Nouns (fallback for names/places not caught by NER)
    NP: {<JJ|NNJ|NUM>*<NNP>+<POST>*}
    
    # 3. Adjective/Adjectival Noun + Common Noun Head Phrase (e.g., "විදෙස් මාධ්‍ය")
    NP: {<JJ|NNJ|NUM>*<NNC>+<POST>*} 

    # 4. Common Nouns with Determiners/Adjectives/Adjectival Nouns
    #    Handles basic common noun phrases.
    NP: {<DET>?<JJ|NNJ|NUM>*<NNC>+<POST>*}

    # 5. Pronouns
    NP: {<PRP.*>+<POST>*}

    # 6. Basic Noun with optional Postposition (catches single nouns or simple nominals)
    NP: {<NN.*><POST>?} 

    # 7. Coordination of Noun Phrases (Combines already identified NPs via CC)
    NP: {<NP><CC><NP>} 
    
    # 8. More aggressive noun phrase catch-all (use with caution, can over-chunk)
    # NP: {<JJ|NNJ|NUM|DET|PRP.*|NN.*>+} # This can be useful as a last resort, but often too greedy.
"""

# VP_GRAMMAR_ENHANCED (Updated in ner_enhanced_triple_extractor.py)

VP_GRAMMAR_ENHANCED = r"""
    # 1. Compound Verb Forms (most common & complex patterns)
    #    These patterns capture the core compound verb structures.
    #    Prioritize NCV/JCV/PCV acting as the initial nominal/adjectival/prepositional part.
    VP: {<NCV|JCV|PCV><VNF>+<VP>+<VFM>+} # e.g., ඝාතනය/NCV කළ/VP බව, but here with a trailing VFM.
                                        # This might be tricky if 'බව' is the end of the clause.
    VP: {<NCV|JCV|PCV><VNF|VP>+<VFM>+}  # e.g., ඝාතනය/NCV කළ/VP තිබේ/VFM
    VP: {<NCV|JCV|PCV><VFM><VFM>+}      # e.g., තීරණය/VFM කර/VFM තිබේ/VFM (if VFM-VFM-VFM)
    VP: {<VNF><VP><VFM>+}               # e.g., ගෙන/VNF තිබෙන/VP (if තිබෙන is VP, this should catch it)

    # 2. Transitive/Intransitive Compound Verbs
    VP: {<VNF><VFM>+}                   # e.g., අත්අඩංගුවට/VNF ගෙන/VNF (if VNF-VNF-VFM compound then VNF VNF) or වාර්තා/VFM කරනවා/VFM
    VP: {<VFM><VFM>+}                   # Simple VFM + VFM sequence. e.g., වාර්තා/VFM කරනවා/VFM

    # 3. Simple Verb Phrases (single verbs or basic sequences)
    VP: {<VFM>+}
    VP: {<VP>+}
    VP: {<VNF>+}
    VP: {<VNN>+}

    # 4. Sentence Ending "Verb-like" words
    VP: {<NVB>+}
"""


CHUNK_GRAMMAR_ENHANCED = f"{NP_GRAMMAR_ENHANCED}\n{VP_GRAMMAR_ENHANCED}"
CHUNK_PARSER_ENHANCED = RegexpParser(CHUNK_GRAMMAR_ENHANCED)

# ... (rest of your file content remains the same) ...

CONSTRAINT1_BOUNDARIES = {"බව", "බවයි"}


class NEREnhancedTripleExtractor:
    """
    Extracts Subject-Verb-Object (SOV) triples from Sinhala news text,
    leveraging AI-based POS tagging and actual NER API output.
    """

    def __init__(self):  # Removed pos_tagger parameter
        # No longer takes pos_tagger as a direct dependency for __init__
        # It relies on the global pos_tagging_simulate function being available.
        print("--- NEREnhancedTripleExtractor Initialized ---")

    def _enhance_pos_with_ner(self, pos_tagged_words: list, ner_results: dict) -> list:
        """
        Merges POS tags with NER information.
        If a word is identified as an entity by NER, its POS tag is augmented.
        e.g., ('ශ්‍රීකාන්ත්', 'NNP') + PERSON -> ('ශ්‍රීකාන්ත්', 'NNP_PERSON')
        """
        enhanced_tags = []

        word_to_entity_map = {}
        for entity_type, entity_list in ner_results.items():
            for entity_text in entity_list:
                for word_part in entity_text.split():
                    word_to_entity_map[word_part] = entity_type.upper().replace(
                        "S", ""
                    )  # Convert 'persons' to 'PERSON' etc.

        for word, pos_tag in pos_tagged_words:
            new_pos_tag = pos_tag
            if word in word_to_entity_map:
                entity_type = word_to_entity_map[word]
                if not pos_tag.endswith(f"_{entity_type}"):
                    if pos_tag == "UNK":
                        new_pos_tag = f"NNP_{entity_type}"
                    else:
                        new_pos_tag = f"{pos_tag}_{entity_type}"
            enhanced_tags.append((word, new_pos_tag))
        return enhanced_tags

    def _apply_constraint1_ner_enhanced(self, chunk_tree: Tree) -> list:
        triples = []
        words = list(chunk_tree.leaves())

        boundary_index = -1
        for i, (word, tag) in enumerate(words):
            if word in CONSTRAINT1_BOUNDARIES and tag == "POST":
                boundary_index = i
                break

        if boundary_index != -1:
            left_side_words = words[:boundary_index]
            right_side_words = words[boundary_index + 1 :]

            left_chunk_tree = CHUNK_PARSER_ENHANCED.parse(left_side_words)
            right_chunk_tree = CHUNK_PARSER_ENHANCED.parse(right_side_words)

            # --- Extract Object from LHS (The clause content / inner event) ---
            # Inner Subject: Prioritize NNP_PERSON/ORG/LOC from LHS NPs
            inner_lhs_subject = "N/A_LHS_Subject"
            lhs_nps = []
            for subtree in left_chunk_tree.subtrees():
                if subtree.label() == "NP":
                    lhs_nps.append(
                        (subtree, " ".join(leaf[0] for leaf in subtree.leaves()))
                    )

            if lhs_nps:
                # Find the best subject candidate in LHS
                # Prioritize: 1. NNP_PERSON/ORG/LOC. 2. Any NNP. 3. First NP.
                best_inner_sub_candidate = None
                for np_tree, np_text in lhs_nps:
                    if any(
                        tag.endswith(("_PERSON", "_ORG", "_LOC", "_EVENT"))
                        for w, t in np_tree.leaves()
                    ):
                        best_inner_sub_candidate = np_text
                        break  # Found a high-priority subject
                if best_inner_sub_candidate is None:
                    for np_tree, np_text in lhs_nps:
                        if any(t.startswith("NNP") for w, t in np_tree.leaves()):
                            best_inner_sub_candidate = np_text
                            break  # Found a general NNP
                inner_lhs_subject = (
                    best_inner_sub_candidate
                    if best_inner_sub_candidate
                    else lhs_nps[0][1]
                )

            # Inner Verb: Find the main VP in LHS
            inner_lhs_verb = "N/A_LHS_Verb"
            lhs_vps = []
            for subtree in left_chunk_tree.subtrees():
                if subtree.label() == "VP":
                    lhs_vps.append(" ".join(leaf[0] for leaf in subtree.leaves()))
            if lhs_vps:
                inner_lhs_verb = lhs_vps[-1]  # Take the last VP

            # Inner Object: Still N/A for now, as it needs deeper transitive verb analysis
            inner_lhs_object = "N/A_LHS_Object"

            outer_object_representation = {
                "type": "event_clause",
                "content_text": " ".join(leaf[0] for leaf in left_side_words).strip(),
                "inner_subject": inner_lhs_subject,
                "inner_verb": inner_lhs_verb,
                "inner_object": inner_lhs_object,
            }

            # --- Extract Subject and Verb from RHS (Main clause) ---
            main_subject_rhs = "N/A_RHS_Subject"
            main_verb_rhs = "N/A_RHS_Verb"

            # Extract NPs and VPs from RHS
            rhs_nps = []
            rhs_vps = []
            for subtree in right_chunk_tree.subtrees():
                if subtree.label() == "NP":
                    rhs_nps.append(
                        (subtree, " ".join(leaf[0] for leaf in subtree.leaves()))
                    )
                elif subtree.label() == "VP":
                    rhs_vps.append(" ".join(leaf[0] for leaf in subtree.leaves()))

            # Select Main Subject from RHS: Prioritize NER-enhanced NP
            if rhs_nps:
                best_main_sub_candidate = None
                for np_tree, np_text in rhs_nps:
                    if any(
                        tag.endswith(("_PERSON", "_ORG", "_LOC", "_EVENT"))
                        for w, t in np_tree.leaves()
                    ):
                        best_main_sub_candidate = np_text
                        break
                if best_main_sub_candidate is None:
                    # Fallback to general NNP or first NP if no specific entity
                    for np_tree, np_text in rhs_nps:
                        if any(t.startswith("NNP") for w, t in np_tree.leaves()):
                            best_main_sub_candidate = np_text
                            break
                main_subject_rhs = (
                    best_main_sub_candidate
                    if best_main_sub_candidate
                    else rhs_nps[0][1]
                )

            # Select Main Verb from RHS: Last VP is usually the main verb
            if rhs_vps:
                main_verb_rhs = rhs_vps[-1]

            triples.append(
                (main_subject_rhs, main_verb_rhs, outer_object_representation)
            )

        return triples

    def _apply_constraint2_ner_enhanced(self, chunk_tree: Tree) -> list:
        triples = []

        noun_phrases_with_data = []  # Store (text, original_leaves_with_enhanced_tags)
        verb_phrases_text = []

        for subtree in chunk_tree.subtrees():
            if subtree.label() == "NP":
                noun_phrases_with_data.append(
                    (" ".join(leaf[0] for leaf in subtree.leaves()), subtree.leaves())
                )
            elif subtree.label() == "VP":
                verb_phrases_text.append(" ".join(leaf[0] for leaf in subtree.leaves()))

        if verb_phrases_text:
            main_verb = verb_phrases_text[-1]  # Take the last VP as main verb

            subject = "N/A_Subject"
            obj = "N/A_Object"

            # 1. Select Subject (prioritize NER entities, then first NP)
            best_subject_candidate = None
            for np_text, np_leaves in noun_phrases_with_data:
                # Corrected line: 't' is the tag from the (w, t) tuple
                if any(
                    t.endswith(("_PERSON", "_ORG", "_LOC", "_EVENT"))
                    for w, t in np_leaves
                ):
                    best_subject_candidate = np_text
                    break
            if best_subject_candidate is None:
                # Fallback: if no NER entity, try general NNP
                for np_text, np_leaves in noun_phrases_with_data:
                    # Corrected line: 't' is the tag from the (w, t) tuple
                    if any(t.startswith("NNP") for w, t in np_leaves):
                        best_subject_candidate = np_text
                        break
            subject = (
                best_subject_candidate
                if best_subject_candidate
                else (
                    noun_phrases_with_data[0][0] if noun_phrases_with_data else subject
                )
            )

            # 2. Select Object (prioritize NER entities NOT already chosen as subject, then subsequent NPs)
            # Filter out the subject NP if it was found
            remaining_nps_data = [
                np_data for np_data in noun_phrases_with_data if np_data[0] != subject
            ]

            if remaining_nps_data:
                best_object_candidate = None
                for np_text, np_leaves in remaining_nps_data:
                    # Corrected line: 't' is the tag from the (w, t) tuple
                    if any(
                        t.endswith(("_PERSON", "_ORG", "_LOC", "_EVENT"))
                        for w, t in np_leaves
                    ):
                        best_object_candidate = np_text
                        break
                obj = (
                    best_object_candidate
                    if best_object_candidate
                    else remaining_nps_data[0][0]
                )

            triples.append((subject, main_verb, obj))

        return triples

    def extract_triple_enhanced(  # Made async
        self, text: str, ner_results: dict, pos_tagger: SinhalaPOSTagger
    ) -> dict:
        """
        Extracts Subject-Verb-Object (SOV) triples from a single Sinhala sentence,
        leveraging AI-based POS tagging and actual NER API output.

        Args:
            text (str): The input Sinhala sentence (raw, or minimally cleaned for NER).

        Returns:
            dict: A dictionary containing:
                - 'original_text': The input text.
                - 'ner_output': The raw output from the NER API.
                - 'pos_tagged_words': The raw POS-tagged output from the AI.
                - 'enhanced_tagged_words': POS tags enhanced with NER info.
                - 'chunk_tree': The NLTK parse tree after chunking (as a string).
                - 'extracted_triples': A list of (subject, verb, object) tuples.
        """
        if not text:
            return {
                "original_text": text,
                "ner_output": {},
                "pos_tagged_words": [],
                "enhanced_tagged_words": [],
                "chunk_tree": "",
                "extracted_triples": [],
            }

        min_cleaned_text = text

        # Step 3: Raw POS Tagging using the AI agent
        pos_tagged_words = pos_tagger.pos_tagging(min_cleaned_text)

        # Step 4: Enhance POS Tags with NER Information
        # Note: self refers to the NEREnhancedTripleExtractor instance
        enhanced_tagged_words = self._enhance_pos_with_ner(
            pos_tagged_words, ner_results
        )

        # Step 5: Chunking (Partial Parsing) on ENHANCED tags
        chunk_tree = CHUNK_PARSER_ENHANCED.parse(enhanced_tagged_words)

        # Step 6: Apply Syntactic Constraints
        triples = self._apply_constraint1_ner_enhanced(chunk_tree)  # Use self

        if not triples:
            triples = self._apply_constraint2_ner_enhanced(chunk_tree)  # Use self

        return {
            "original_text": text,
            "ner_output": ner_results,
            "pos_tagged_words": pos_tagged_words,
            "enhanced_tagged_words": enhanced_tagged_words,
            "chunk_tree": str(chunk_tree),
            "extracted_triples": triples,
        }
