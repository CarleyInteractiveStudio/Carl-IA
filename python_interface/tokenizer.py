class SimpleTokenizer:
    """
    A simple tokenizer that builds a vocabulary and converts text to sequences of token IDs.
    """
    def __init__(self, oov_token="<UNK>"):
        self.word_index = {}
        self.index_word = {}
        self.oov_token = oov_token
        # Add padding and out-of-vocabulary tokens to the vocabulary
        self.fit([oov_token, "<PAD>"])

    def fit(self, texts):
        """
        Builds or updates the vocabulary from a list of texts.

        Args:
            texts (list of str): A list of sentences or documents.
        """
        for text in texts:
            for word in text.lower().split():
                if word not in self.word_index:
                    index = len(self.word_index)
                    self.word_index[word] = index
                    self.index_word[index] = word

    def tokenize(self, text):
        """
        Converts a single text into a sequence of token IDs.

        Args:
            text (str): The input sentence or document.

        Returns:
            list of int: A list of token IDs.
        """
        oov_index = self.word_index.get(self.oov_token)
        return [
            self.word_index.get(word, oov_index)
            for word in text.lower().split()
        ]

    @property
    def vocab_size(self):
        """Returns the total number of unique tokens in the vocabulary."""
        return len(self.word_index)
