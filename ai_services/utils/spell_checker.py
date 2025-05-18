from spellchecker import SpellChecker

class TextReadabilityChecker:
    def __init__(self):
        """Initialize spell-checker objects for English and Arabic."""
        self.spell_checkers = {
            'en': SpellChecker(),
            'ar': SpellChecker(language='ar')
        }

    def check_text_readability(self, text, language):
        """
        Check the readability of text for a specified language.
        :param text: Text to check.
        :param language: Language of the text ('en' for English, 'ar' for Arabic).
        :return: Tuple (ratio, true_count, readable), where:
                 ratio: Float representing the percentage of correctly spelled words.
                 true_count: Integer indicating the number of correctly spelled words.
                 readable: Boolean indicating whether the text is readable.
        """
        # Get the spell checker for the specified language
        spell = self.spell_checkers.get(language)
        if not spell:
            raise ValueError(f"Unsupported language '{language}'. Use 'en' for English or 'ar' for Arabic.")

        # Split the text into words
        words = text.split()

        # Find misspelled words
        misspelled = spell.unknown(words)

        # Calculate counts
        true_count = len(words) - len(misspelled)  # Correctly spelled words
        false_count = len(misspelled)  # Misspelled words

        # Calculate the ratio of correctly spelled words
        total_words = true_count + false_count
        ratio = true_count / total_words if total_words else 0  # Avoid division by zero

        # Determine if the text is readable
        readable = false_count < true_count

        return ratio, true_count, readable