from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Tải model và tokenizer
model_name = "hang1704/opendaisy"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Hàm dự đoán
def predict(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    product_prob = probs[0][1].item()
    return "product" if product_prob > 0.5 else "chitchat", product_prob

# Đoạn hội thoại
conversations = [
    "Human: Tôi muốn một chiếc điện thoại có camera tốt và pin trâu, giá khoảng 10 triệu đồng.",
    "AI: Hiểu rồi! Với yêu cầu của bạn, tôi có thể gợi ý một vài mẫu điện thoại phù hợp. Ví dụ như Xiaomi Redmi Note 12 Pro hoặc Samsung Galaxy A54. Cả hai đều có camera chất lượng tốt và pin dung lượng lớn. Bạn có muốn biết thêm chi tiết về các mẫu này không?",
    "Human: Có, tôi muốn biết thêm về Xiaomi Redmi Note 12 Pro.",
    "AI: Tuyệt! Xiaomi Redmi Note 12 Pro có camera chính 108MP, pin 5000mAh với sạc nhanh 67W. Màn hình AMOLED 6.67 inch, tần số quét 120Hz. Giá khoảng 8-9 triệu đồng, phù hợp ngân sách của bạn. Bạn nghĩ sao về mẫu này?"
]

conversation_text = "\n".join(conversations)
print(conversation_text)
print("\nĐang phân tích...")

try:
    # Dự đoán
    result, confidence = predict(conversation_text)

    print(f"\nDự đoán cuối cùng:")
    print(f"Loại: {result}")
    if result == "product":
        print(f"Độ tin cậy (product): {confidence*100:.2f}%")
    else:
        print(f"Độ tin cậy (chitchat): {(1-confidence)*100:.2f}%")
except Exception as e:
    print(f"Có lỗi xảy ra: {str(e)}")
    print("Vui lòng kiểm tra lại mô hình và dữ liệu đầu vào.")
