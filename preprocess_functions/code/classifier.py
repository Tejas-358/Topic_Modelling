def predict_labels_for_pdf(pdf_path):
    # Load the pre-trained classification model
    model_file = "model1.json"
    weights_file = "model1.h5"

    with open(model_file, 'r') as json_file:
        loaded_model_json = json_file.read()

    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(weights_file)

    # Load tokenizer configuration
    tokenizer_config_file = 'tokenizer_config.json'

    with open(tokenizer_config_file) as json_file:
        tokenizer_config = json.load(json_file)

    loaded_tokenizer = Tokenizer()
    loaded_tokenizer.word_index = tokenizer_config['word_index']
    loaded_tokenizer.word_counts = tokenizer_config['word_counts']
    loaded_tokenizer.index_word = tokenizer_config['index_word']
    loaded_tokenizer.index_docs = tokenizer_config['index_docs']

    # Load MultiLabelBinarizer
    mlb_file = "mlb1.pkl"
    loaded_mlb = joblib.load(mlb_file)

    # Process the PDF
    pdf = PyPDF2.PdfReader(open(pdf_path, "rb"))
    all_paragraphs = []

    for page in pdf.pages:
        page_text = page.extract_text()
        all_paragraphs.extend(page_text.split('\n'))

    preprocessed_paragraphs = preprocess_paragraphs(split_into_paragraphs(all_paragraphs))

    predicted_labels = []
    for paragraph in preprocessed_paragraphs:
        preprocessed_text = ' '.join(paragraph)
        text_sequence = loaded_tokenizer.texts_to_sequences([preprocessed_text])
        padded_sequence = pad_sequences(text_sequence, maxlen=200)  # Adjust max sequence length as needed

        paragraph_labels_bin = loaded_model.predict(padded_sequence)
        paragraph_labels = loaded_mlb.inverse_transform(paragraph_labels_bin > 0.5)  # Adjust threshold as needed

        # Collect labels for the paragraph and flatten the list
        flat_labels = [label for labels in paragraph_labels for label in labels]
        predicted_labels.append(flat_labels)

    return predicted_labels


if __name__ == "__main__":
    # Replace 'your_pdf.pdf' with the path to your PDF file
    user_uploaded_pdf_path = 'your_pdf.pdf'
    predicted_labels = predict_labels_for_pdf(user_uploaded_pdf_path)

    for i, labels in enumerate(predicted_labels):
        print(f"Labels for Paragraph {i + 1}: {', '.join(labels)}")