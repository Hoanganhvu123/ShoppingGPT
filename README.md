ShoppingGPT 🛒🤖
ShoppingGPT là một trợ lý mua sắm thông minh được thiết kế để giúp người dùng truy vấn dữ liệu sản phẩm được lưu trữ trong tệp CSV. Dự án này tận dụng sức mạnh của Python, Pandas và một mô hình ngôn ngữ tiên tiến (LLM) để cung cấp thông tin chi tiết về các sản phẩm khác nhau.

Tính Năng ✨
🔍 Product Information Retrieval: Truy xuất thông tin chi tiết về sản phẩm dựa trên truy vấn của người dùng.
🔤 Case-Insensitive Search: Xử lý tên sản phẩm không phân biệt chữ hoa chữ thường và cho phép khớp một phần.
⚡ Efficient Data Processing: Sử dụng các kỹ thuật lập chỉ mục và lọc hiệu quả để xử lý dữ liệu.
🔄 Data Conversion: Chuyển đổi các giá trị chuỗi thành số thực cho cột 'price' nếu cần thiết.
🛡️ Error Handling: Xác thực đầu vào để ngăn ngừa các lỗi tiềm ẩn.
Cấu Trúc Dữ Liệu 🗂️
Dữ liệu sản phẩm được lưu trữ trong tệp CSV và được tải vào một DataFrame của Pandas với các cột sau:

product_code: Một mã định danh duy nhất cho mỗi sản phẩm (chuỗi)
product_name: Tên của sản phẩm (chuỗi)
material: Thành phần vật liệu của sản phẩm (chuỗi)
size: Kích thước của sản phẩm (chuỗi)
color: Màu sắc của sản phẩm (chuỗi)
brand: Thương hiệu sản xuất hoặc bán sản phẩm (chuỗi)
gender: Giới tính mục tiêu của sản phẩm (ví dụ: nam, nữ, unisex) (chuỗi)
stock_quantity: Số lượng sản phẩm có sẵn trong kho (số nguyên)
price: Giá của sản phẩm, có thể là chuỗi hoặc giá trị số (chuỗi hoặc số)
Cài Đặt 🛠️
Để sử dụng ShoppingGPT, hãy thực hiện các bước sau:

Clone repository:

bash
Copy code
git clone https://github.com/Hoanganhvu123/ShoppingGPT.git
cd ShoppingGPT
Tạo và kích hoạt môi trường ảo:

bash
Copy code
python -m venv venv
source venv/bin/activate  # Trên Windows, sử dụng `venv\Scripts\activate`
Cài đặt các thư viện cần thiết:

bash
Copy code
pip install -r requirements.txt
Sử Dụng 🖥️
Chạy Backend
Điều hướng đến thư mục backend/app:

bash
Copy code
cd backend/app
Chạy ứng dụng FastAPI với Uvicorn:

bash
Copy code
uvicorn main:app --reload
Chạy Frontend
Điều hướng đến thư mục frontend:

bash
Copy code
cd frontend
Chạy ứng dụng React:

bash
Copy code
npm install
npm run dev