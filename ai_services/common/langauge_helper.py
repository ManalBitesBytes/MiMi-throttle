def detect_language(text: str):
    """
    Detect the language(s) of a string without external libraries.
    • Returns ['ar']  → mostly Arabic letters
    • Returns ['en']  → mostly English letters
    • Returns ['ar', 'en'] → mixed (roughly 40-60 % each)
    • Returns []      → no Arabic or English letters found
    """
    if not text:
        return []

    # Unicode ranges that contain Arabic letters
    arabic_ranges = [
        (0x0600, 0x06FF),   # Arabic
        (0x0750, 0x077F),   # Arabic Supplement
        (0x08A0, 0x08FF),   # Arabic Extended-A
        (0xFB50, 0xFDFF),   # Arabic Presentation Forms-A
        (0xFE70, 0xFEFF),   # Arabic Presentation Forms-B
        (0x1EE00, 0x1EEFF)  # Arabic Mathematical Alphabet
    ]

    def is_arabic(ch):
        cp = ord(ch)
        return any(start <= cp <= end for start, end in arabic_ranges)

    def is_english(ch):
        return ('A' <= ch <= 'Z') or ('a' <= ch <= 'z')

    arabic_count  = sum(1 for ch in text if is_arabic(ch))
    english_count = sum(1 for ch in text if is_english(ch))

    total = arabic_count + english_count
    if total == 0:
        return []

    arabic_ratio = arabic_count / total
    english_ratio = english_count / total

    # Simple decision rules
    if 0.4 <= arabic_ratio <= 0.6:
        return ['ar', 'en']             # fairly balanced mixture
    elif arabic_ratio > english_ratio:
        return ['ar']
    else:
        return ['en']
