import re
import unicodedata


def basic_clean_text(text):
    if not text or str(text) == 'nan':
        text = ''
    text = re.sub("[^a-zA-Z0-9]+", " ", text)
    text = re.sub('  +', ' ', text)
    text = text.strip()
    return text


def clean_text_artifacts(text):
    """
    Clean the input text by removing unwanted characters and normalizing whitespace.
    """
    clean_text = re.sub(r'\n+', '\n', text).replace("\r", "\n").replace("\t",
                                                                        " ")  # Replace multiple newlines with a single newline, replace carriage returns with newlines, replace tabs with spaces
    clean_text = re.sub(r"\uf0b7", " ", clean_text)  # Remove specific Unicode character used as a bullet point
    clean_text = re.sub(r"\(cid:\d{0,2}\)", " ", clean_text)  # Remove encoding artifacts from PDF conversions
    clean_text = re.sub(r'• ', " ", clean_text)  # Remove bullet points followed by a space
    resume_lines = clean_text.splitlines(True)
    resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if
                    line.strip()]  # Split into lines, normalize whitespace, and remove empty lines
    return resume_lines


def llm_clean_text(text):
    # Define a regex pattern to match Arabic characters, English letters, and numbers
    pattern = re.compile(r'[a-zA-Z0-9\u0600-\u06FF\s]+')

    # Find all matches in the text
    matches = pattern.findall(text)

    # Join the matches into a single string
    cleaned_text = ' '.join(matches)
    cleaned_text = re.sub(r'[\n\t]+', '\n\n', cleaned_text)

    return cleaned_text


def remove_special_characters(text):
    # Replace special characters with an empty string
    cleaned_text = re.sub(r'[^A-Za-z0-9]+', '', text)
    return cleaned_text


def contains_english(text):
    # Search for at least one English character (a-z or A-Z)
    return bool(re.search(r'[a-zA-Z]', text))


def translation_english_text_normalization(text):
    # Step 1: Strip leading and trailing spaces
    normalized_text = text.strip()

    # Step 2: Normalize Unicode to remove accents and diacritics
    normalized_text = ''.join(
        c for c in unicodedata.normalize('NFD', normalized_text) if unicodedata.category(c) != 'Mn')

    # Step 3: Replace special characters except letters, numbers, periods, and plus signs
    normalized_text = re.sub(r'[^a-zA-Z0-9\.\+\s]', ' ', normalized_text)

    # Step 4: Replace multiple spaces with a single space
    normalized_text = re.sub(r'\s+', ' ', normalized_text).strip()

    # Step 5: Split the text into words to process each word individually
    words = normalized_text.split()

    # Step 6: Capitalize each word, unless the word has two or more consecutive uppercase letters (to preserve acronyms)
    processed_words = []
    for word in words:
        if re.match(r'^[A-Z]{2,}$', word):  # Acronyms like NASA, USA, etc.
            processed_words.append(word)  # Preserve acronyms in uppercase
        else:
            processed_words.append(word.capitalize())  # Capitalize other words

    # Step 7: Join the words back into a single string
    normalized_text = ' '.join(processed_words)

    return normalized_text


def advanced_clean_text(raw_text):
    if not raw_text:
        return raw_text

    # Substitute URLs with an empty string
    raw_text = re.sub(r'https?://\S+|www\.\S+', '', raw_text)

    raw_text = re.sub(r'\b\w{50,}\b', ' ', raw_text)
    raw_text = re.sub(r'(\s{3,}|\n{2,})', ' ', raw_text)
    return raw_text
