from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Constants
PRODUCT_ROUTE_NAME = 'products'
CHITCHAT_ROUTE_NAME = 'chitchat'

class SemanticRouter:
    def __init__(self):
        # Tải model và tokenizer
        model_name = "hang1704/opendaisy"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        product_prob = probs[0][1].item()
        return PRODUCT_ROUTE_NAME if product_prob > 0.5 else CHITCHAT_ROUTE_NAME, product_prob

    def guide(self, query: str) -> str:
        result, confidence = self.predict(query)
        return result

