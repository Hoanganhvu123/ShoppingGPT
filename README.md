<<<<<<< HEAD
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
=======
# ShoppingGPT 🛒🤖

ShoppingGPT is an intelligent shopping assistant designed to help users query product data stored in a CSV file. This project leverages the power of Python, Pandas, and an advanced Language Learning Model (LLM) to provide detailed information about various products.

## Features ✨

- 🔍 **Product Information Retrieval**: Retrieve detailed information about products based on user queries.
- 🔤 **Case-Insensitive Search**: Handle product names in a case-insensitive manner and allow for partial matches.
- ⚡ **Efficient Data Processing**: Utilize efficient indexing and filtering techniques to process data.
- 🔄 **Data Conversion**: Convert string values to float for the 'price' column if necessary.
- 🛡️ **Error Handling**: Validate input to prevent potential errors.

## Data Structure 🗂️

The product data is stored in a CSV file and loaded into a Pandas DataFrame with the following columns:

- `product_code`: A unique identifier for each product (string)
- `product_name`: The name of the product (string)
- `material`: The material composition of the product (string)
- `size`: The size of the product (string)
- `color`: The color of the product (string)
- `brand`: The brand that manufactures or sells the product (string)
- `gender`: The target gender for the product (e.g., male, female, unisex) (string)
- `stock_quantity`: The quantity of the product available in stock (integer)
- `price`: The price of the product, which can be a string or numeric value (string or numeric)

## Installation 🛠️

To use ShoppingGPT, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Hoanganhvu123/ShoppingGPT.git
    cd ShoppingGPT
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage 🖥️

### Running the Backend

1. Navigate to the `backend/app` directory:
    ```bash
    cd backend/app
    ```

2. Run the FastAPI application with Uvicorn:
    ```bash
    uvicorn main:app --reload
    ```

### Running the Frontend

1. Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```

2. Run the React application:
    ```bash
    npm install
    npm run dev
    ```

## Screenshots 🌟

### Website with Integrated Chatbot

Your website will look like this with the Chatbot integrated in the bottom right corner:

![image](https://github.com/user-attachments/assets/8337a3c3-9bec-405b-aff6-64af5d6a346f)

![image](https://github.com/user-attachments/assets/fe601030-a688-4f44-a642-683324c9624e)

![image](https://github.com/user-attachments/assets/d0a1b9ae-28f5-4048-be73-00e9709da769)


### Chatbot Interface

The Chatbot helps users query product information easily and intuitively:

![image](https://github.com/user-attachments/assets/0b100e4e-697f-46a5-9b60-c723925418c6)


## Technical Details 🔧

### Backend

The backend of ShoppingGPT is built with FastAPI, a modern and fast web framework for building APIs with Python 3.7+.

#### Backend Directory Structure

- **`app/`**: Contains the main source code for the FastAPI application.
  - **`main.py`**: The main entry point of the application, initializing and running FastAPI.
  - **`api/`**: Contains the API routers and endpoints.
    - **`chatbot/`**: Contains source code related to chatbot functionality.
  - **`core/`**: Contains configuration and settings for the application.
  - **`services/`**: Contains services and main processing logic for the application.
  - **`utils/`**: Contains utilities and helper functions.

### Frontend

The frontend of ShoppingGPT is built with React, a popular JavaScript library for building user interfaces.

#### Frontend Directory Structure

- **`src/`**: Contains the main source code for the React application.
  - **`Components/Chatbot/Chatbot.js`**: The main component for the Chatbot.
  - **`index.js`**: The main entry point of the React application.

## Feedback and Contributions 🌟

If you have any feedback or contributions, please open an issue or pull request on the [GitHub repository](https://github.com/Hoanganhvu123/ShoppingGPT).

## License 📄

This project is licensed under the MIT License. See the LICENSE file for more details.

## Author 👨‍💻

ShoppingGPT is developed by [Hoanganhvu123](https://github.com/Hoanganhvu123). If you have any questions, feel free to contact me via email or open an issue on GitHub.

## Contact 📬

If you have any questions or need support, please contact me at:

- Email: hoanganhvu123@example.com
- GitHub: [Hoanganhvu123](https://github.com/Hoanganhvu123)
- LinkedIn: [Hoanganh Vu](https://www.linkedin.com/in/hoanganhvu)

## Conclusion 🏁

ShoppingGPT is an exciting project with the potential to develop intelligent features for online shopping. Combining Python, Pandas, FastAPI, and React, this project provides a powerful and flexible platform to build smart shopping applications.

Thank you for using ShoppingGPT! I hope you have a great shopping experience and success with your projects!
>>>>>>> 9c5ad01b124ff9add5f4df4af6fe8129b8a04823
