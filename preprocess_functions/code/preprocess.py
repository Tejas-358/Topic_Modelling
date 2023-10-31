

def text_preprocessing(text):
    # Remove non-ASCII characters
    text = ''.join([c if ord(c) < 128 else ' ' for c in text])

    # Remove Roman numerals using a regular expression
    text = re.sub(r'\b[IVXLCDM]+(?:\s+[ivxlcdm]+)?\b', '', text)  # Remove lowercase Roman numerals

    # Convert to lowercase
    text = text.lower()
    text = text.replace('“', '')
    text = text.replace('”', '')
    text = text.replace('’', '')
    text = text.replace('\n', ' ').replace('-', ' ')
    text = re.sub(r'\d+', '', text)  # Remove digits
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r',+', ',  ,', text)

    # Tokenize the text and remove stopwords
    words = word_tokenize(text)
    words = [word for word in words if word not in stopwords.words('english')]
    text = ' '.join(words)

    return text

# Function for preprocessing paragraphs
def preprocess_paragraphs(paragraphs):
    preprocessed_paragraphs = []
    for paragraph in paragraphs:
        preprocessed_paragraph = [text_preprocessing(line) for line in paragraph]
        preprocessed_paragraphs.append(preprocessed_paragraph)
    return preprocessed_paragraphs

# Function for splitting text into paragraphs
def split_into_paragraphs(text_list, lines_per_paragraph=8):
    paragraphs = []

    for text in text_list:
        current_paragraph = []
        lines_in_current_paragraph = 0

        for line in text.split("\n"):
            current_paragraph.append(line)
            lines_in_current_paragraph += 1

            if lines_in_current_paragraph == lines_per_paragraph:
                paragraphs.append(current_paragraph)
                current_paragraph = []
                lines_in_current_paragraph = 0

        # Add the remaining lines in the current paragraph to the list of paragraphs.
        if current_paragraph:
            paragraphs.append(current_paragraph)

    return paragraphs