from transformers import pipeline


bart_large_cnn_model = pipeline("summarization", model="facebook/bart-large-cnn")