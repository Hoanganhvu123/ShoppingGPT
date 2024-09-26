import os
import time
import random
import json
import asyncio
import aiohttp
from typing import List, Optional
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema import AIMessage

# Tải biến môi trường
load_dotenv()

GROQ_API_KEYS = ["Your API Key"]

# Danh sách các mô hình Groq và giới hạn của chúng
GROQ_MODELS = [
    {"name": "gemma-7b-it", "rpm": 30, "tpm": 14400, "max_tokens": 15000, "daily_limit": 500000},
    {"name": "gemma2-9b-it", "rpm": 30, "tpm": 14400, "max_tokens": 15000, "daily_limit": 500000},
    {"name": "llama-3.1-70b-versatile", "rpm": 30, "tpm": 14400, "max_tokens": 20000, "daily_limit": 500000},
    {"name": "llama-3.1-8b-instant", "rpm": 30, "tpm": 14400, "max_tokens": 20000, "daily_limit": 500000},
    {"name": "llama3-70b-8192", "rpm": 30, "tpm": 14400, "max_tokens": 6000, "daily_limit": 500000},
    {"name": "llama3-8b-8192", "rpm": 30, "tpm": 14400, "max_tokens": 30000, "daily_limit": 500000},
    {"name": "llama3-groq-70b-8192-tool-use-preview", "rpm": 30, "tpm": 14400, "max_tokens": 15000, "daily_limit": 500000},
    {"name": "llama3-groq-8b-8192-tool-use-preview", "rpm": 30, "tpm": 14400, "max_tokens": 15000, "daily_limit": 500000},
    {"name": "mixtral-8x7b-32768", "rpm": 30, "tpm": 14400, "max_tokens": 5000, "daily_limit": 500000},
    {"name": "llama-3.2-11b-text-preview", "rpm": 30, "tpm": 7000, "max_tokens": 7000, "daily_limit": 500000},
    {"name": "llama-3.2-1b-preview", "rpm": 30, "tpm": 7000, "max_tokens": 7000, "daily_limit": 500000},
    {"name": "llama-3.2-3b-preview", "rpm": 30, "tpm": 7000, "max_tokens": 7000, "daily_limit": 500000},
    {"name": "llama-3.2-90b-text-preview", "rpm": 30, "tpm": 7000, "max_tokens": 7000, "daily_limit": 500000},
]

class ModelManager:
    def __init__(self):
        self.last_request_time = {model['name']: {key: 0 for key in GROQ_API_KEYS} for model in GROQ_MODELS}
        self.requests_this_minute = {model['name']: {key: 0 for key in GROQ_API_KEYS} for model in GROQ_MODELS}

    async def can_make_request(self, model_name: str, api_key: str) -> bool:
        current_time = time.time()
        if current_time - self.last_request_time[model_name][api_key] >= 60:
            self.requests_this_minute[model_name][api_key] = 0
            self.last_request_time[model_name][api_key] = current_time
        model_info = next(model for model in GROQ_MODELS if model['name'] == model_name)
        return self.requests_this_minute[model_name][api_key] < model_info['rpm']

    async def increment_request(self, model_name: str, api_key: str) -> None:
        self.requests_this_minute[model_name][api_key] += 1

def create_prompt(category: str) -> str:
    prompts = f"""
Bạn là trợ lý ảo. Tạo cuộc hội thoại ngắn về chủ đề: {category}.
Hãy đảm bảo cuộc trò chuyện có nhiều lượt qua lại và đa dạng nội dung

Hãy tạo một cuộc trò chuyện ngẫu nhiên và độc đáo, không lặp lại các mẫu câu hoặc ý tưởng đã sử dụng trước đó.
Sử dụng ngôn ngữ tự nhiên, thân thiện và phù hợp với ngữ cảnh.
Đảm bảo có ít nhất 3-4 lượt trao đổi qua lại giữa Human và AI.
Sinh cuộc hội thoại bằng tiếng Việt.

Ví dụ minh họa cho category "chitchat":
Human: Chào bạn! Hôm nay thời tiết thế nào?
AI: Xin chào! Hôm nay trời nắng đẹp lắm, nhiệt độ khoảng 25 độ C, rất thích hợp để đi dạo công viên. Bạn có kế hoạch gì cho ngày hôm nay không?
Human: Tôi đang nghĩ đến việc đọc một cuốn sách hay. Bạn có gợi ý gì không?
AI: Ồ, đọc sách là một ý tưởng tuyệt vời! Tôi có thể gợi ý cho bạn cuốn "Người giàu có nhất thành Babylon" của George S. Clason. Đó là một cuốn sách rất hay về quản lý tài chính cá nhân. Bạn thích thể loại sách nào nhất?
Human: Tôi thích đọc sách về phát triển bản thân. Bạn có đề xuất nào khác không?
AI: Tuyệt vời! Nếu bạn thích sách về phát triển bản thân, tôi nghĩ bạn sẽ thích cuốn "Đắc Nhân Tâm" của Dale Carnegie. Nó chứa đựng nhiều bài học quý giá về cách giao tiếp và xây dựng mối quan hệ. Hoặc nếu bạn muốn tập trung vào việc xây dựng thói quen tốt, "Sức Mạnh Của Thói Quen" của Charles Duhigg cũng là một lựa chọn tuyệt vời.

Ví dụ minh họa khác cho category "chitchat":
Human: Chào bạn! Bạn có biết món ăn truyền thống nào của Việt Nam không?
AI: Xin chào! Ồ, Việt Nam có rất nhiều món ăn truyền thống ngon tuyệt. Một trong những món nổi tiếng nhất là phở - một loại súp mì với nước dùng thơm ngon và thịt bò hoặc gà. Bạn đã từng thử phở chưa?
Human: Tôi đã thử phở rồi, rất ngon! Còn món nào khác nữa không?
AI: Tuyệt vời! Tôi rất vui khi bạn đã thích phở. Một món khác mà bạn có thể thử là bánh mì - một loại sandwich độc đáo của Việt Nam. Nó kết hợp giữa ảnh hưởng của Pháp (bánh mì) và nguyên liệu đặc trưng của Việt Nam như rau thơm, đồ chua, và các loại thịt. Bạn có thích ăn đồ cay không? Nếu có, tôi còn một gợi ý tuyệt vời nữa đấy!
Human: Có, tôi thích đồ cay! Bạn định gợi ý món gì vậy?
AI: Tuyệt quá! Vậy thì bạn nhất định phải thử bún bò Huế. Đây là một món súp cay, đậm đà từ miền Trung Việt Nam. Nó có sợi bún to, thịt bò, giò heo, và nước dùng cay nồng từ sả và ớt. Hương vị phức tạp và cay nồng của nó chắc chắn sẽ làm bạn thích thú. Bạn có muốn biết cách làm món này không? Tôi có thể chia sẻ một công thức đơn giản đấy!

Ví dụ minh họa cho category "product":
Human: Chào bạn, tôi đang tìm một chiếc áo khoác cho mùa đông.
AI: Xin chào! Rất vui được hỗ trợ bạn. Bạn đang tìm kiếm loại áo khoác như thế nào? Áo khoác lông vũ, áo khoác dạ, hay áo khoác da chẳng hạn?
Human: Tôi nghĩ áo khoác lông vũ sẽ phù hợp. Bạn có gợi ý gì không?
AI: Tuyệt vời! Áo khoác lông vũ là lựa chọn tuyệt vời cho mùa đông. Chúng tôi có một số mẫu áo khoác lông vũ mới nhất từ thương hiệu ABC, rất nhẹ nhưng giữ ấm cực tốt. Bạn thích màu gì và kích cỡ của bạn là bao nhiêu?
Human: Tôi thích màu xanh đậm và mặc size M. Bạn có mẫu nào phù hợp không?
AI: Tuyệt vời! Chúng tôi có một mẫu áo khoác lông vũ màu xanh đậm của ABC, model XYZ123, size M rất phù hợp với yêu cầu của bạn. Áo này có thiết kế hiện đại, khóa kéo hai chiều tiện lợi, và có thể gấp gọn vào túi riêng khi không sử dụng. Nó cũng có công nghệ chống thấm nước, giúp bạn luôn khô ráo trong thời tiết ẩm ướt. Bạn có muốn xem hình ảnh và thông tin chi tiết về sản phẩm này không?

Ví dụ minh họa khác cho category "product":
Human: Chào, tôi đang tìm một đôi giày chạy bộ tốt.
AI: Xin chào! Rất vui được hỗ trợ bạn tìm giày chạy bộ. Bạn thường chạy trên địa hình nào? Đường phố, đường mòn hay sân tập thể dục? Và bạn có yêu cầu đặc biệt nào về độ đệm hay hỗ trợ cho bàn chân không?
Human: Tôi thường chạy trên đường phố và cần giày có độ đệm tốt vì tôi hay bị đau gót chân.
AI: Tôi hiểu rồi. Với nhu cầu của bạn, tôi nghĩ đôi giày DEF Runner Pro sẽ rất phù hợp. Nó có công nghệ đệm CloudFoam ở phần gót, giúp giảm áp lực lên gót chân khi chạy trên bề mặt cứng như đường phố. Đế giày cũng có độ bám tốt và khả năng chống trơn trượt. Bạn thường mang size giày nào và bạn thích màu sắc nào nhất?
Human: Tôi mang size 42 và thích màu xám hoặc đen.
AI: Tuyệt vời! Chúng tôi có sẵn DEF Runner Pro size 42 trong cả hai màu xám và đen. Màu xám có điểm nhấn màu bạc rất thời trang, trong khi màu đen có các chi tiết phản quang giúp tăng độ an toàn khi chạy vào buổi tối. Cả hai đều có giá là 1,500,000 đồng. Bạn muốn xem hình ảnh chi tiết của màu nào trước?

Conversation:
Human: Xin chào!
AI: """
    return prompts

async def generate_conversation(session: aiohttp.ClientSession, llm: ChatGroq, prompt: PromptTemplate) -> str:
    chain = prompt | llm
    return await chain.ainvoke({})

async def generate_data(session: aiohttp.ClientSession, api_key: str, model_name: str, model_manager: ModelManager, categories: List[str], total_data: int, data_queue: asyncio.Queue) -> None:
    while True:
        if await model_manager.can_make_request(model_name, api_key):
            llm = ChatGroq(temperature=0.9, model=model_name, groq_api_key=api_key, client=session)
            category = random.choice(categories)
            prompt = PromptTemplate(input_variables=[], template=create_prompt(category))
            
            try:
                conversation = await generate_conversation(session, llm, prompt)
                await model_manager.increment_request(model_name, api_key)
                
                ai_response = conversation.content if isinstance(conversation, AIMessage) else str(conversation)
                cleaned_response = ai_response.replace("Human:", "\nHuman:").replace("AI:", "\nAI:").strip()
                
                data = {
                    "conversation": cleaned_response,
                    "category": category
                }
                await data_queue.put(data)
                print(f"Generated ({category}) using {model_name} with API key {api_key[-4:]}:\n{cleaned_response}\n---")
                
                if data_queue.qsize() >= total_data:
                    return
            except Exception as e:
                print(f"Error with model {model_name} and API key {api_key[-4:]}: {str(e)}")
        else:
            await asyncio.sleep(1)

async def append_to_json(data: List[dict], filename: str = "synthetic_conversations.json") -> None:
    existing_data = []
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {filename} is empty or contains invalid JSON. Starting with an empty list.")
    
    existing_data.extend(data)
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
    
    print(f"Đã thêm {len(data)} hội thoại mới vào file {filename}. Tổng số hội thoại: {len(existing_data)}.")

async def main() -> None:
    model_manager = ModelManager()
    categories = ["product", "chitchat"]
    total_data = 1000
    data_queue: asyncio.Queue = asyncio.Queue()
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for api_key in GROQ_API_KEYS:
            for model in GROQ_MODELS:
                task = asyncio.create_task(generate_data(session, api_key, model['name'], model_manager, categories, total_data, data_queue))
                tasks.append(task)
        
        all_data = []
        while len(all_data) < total_data:
            data = await data_queue.get()
            all_data.append(data)
            if len(all_data) >= total_data:
                for task in tasks:
                    task.cancel()
                break
        
        await append_to_json(all_data[:total_data])

if __name__ == "__main__":
    asyncio.run(main())
