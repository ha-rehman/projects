import re
import torch
import pickle
import numpy as np
from transformers import BertTokenizer
from tensorflow.keras.models import load_model
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')


def clean_text(text):
    text = text.replace('[^\w\s]', '')  # getting rid of special characters
    text = text.replace('\d+', '')  # removing numeric values from between the words
    text = re.sub(r'\d+', '', text)  # removing numerical numbers
    text = " ".join(x.lower() for x in text.split())  # lower case conversion
    stop = stopwords.words('english')
    text = " ".join(x for x in text.split() if x not in stop)  # removing stop words
    stemmer = WordNetLemmatizer()
    text = " ".join([stemmer.lemmatize(word) for word in text.split()])  # converting words to their dictionary form
    return text


def sarcasm_detection(text):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
    max_len = 64  # Maximum sequence length

    encoded_dict = tokenizer.encode_plus(
        text,  # Text to encode.
        add_special_tokens=True,  # Add '[CLS]' and '[SEP]'
        max_length=max_len,  # Pad & truncate all sentences.
        pad_to_max_length=True,
        return_attention_mask=True,  # Construct attn. masks.
        return_tensors='pt',  # Return pytorch tensors.
    )

    # Load the trained model from its saved state
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    input_ids = encoded_dict['input_ids'].to(device)
    attention_masks = encoded_dict['attention_mask'].to(device)

    model = torch.load('BERT.pt', map_location=torch.device(device))

    # Make the prediction
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_masks)
        _, predicted = torch.max(outputs[0], 1)

    # Convert the predicted label to text
    predicted_label = "Yes" if predicted.item() == 1 else "No"
    return predicted_label


def subtype_detection(text):
    with open('tfidf_vectorizer.pkl', 'rb') as f:
        loaded_tfidf_vectorizer = pickle.load(f)

    text_sample_vector = loaded_tfidf_vectorizer.transform([text]).toarray()[0]
    text_sample_vector = np.reshape(text_sample_vector, (1, 200))

    # Load the model and made predictions
    loaded_model = load_model('my_model.h5')
    predictions = loaded_model.predict(text_sample_vector)

    # Convert the predicted probabilities to binary labels
    binary_pred = (predictions > 0.5).astype(int)
    binary_pred = np.array(binary_pred[0])

    target_names = np.array(['sarcasm',
                             'irony',
                             'satire',
                             'understatement',
                             'overstatement',
                             'rhetorical_question'])

    sample_labels = list(target_names[binary_pred == 1])
    sample_labels = ' , '.join(sample_labels) if len(sample_labels) > 1 else sample_labels[0]
    return sample_labels


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sarcasm_detection('Sample text for detection')
