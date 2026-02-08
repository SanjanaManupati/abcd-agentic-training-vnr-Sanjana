import re

def simple_tokenizer(text):
    # Convert to lowercase
    text = text.lower()

    # Remove punctuation using regex
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Split by whitespace
    tokens = text.split()

    return tokens


# Example usage
if __name__ == "__main__":
    sentence = "Hello! I am learning Tokenization in AI, and it's fun."
    tokens = simple_tokenizer(sentence)
    print("Tokens:", tokens)
