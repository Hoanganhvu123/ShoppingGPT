# ShoppingGPT 🛍️🤖

ShoppingGPT is an advanced AI-powered shopping assistant that combines cutting-edge natural language processing techniques to provide a seamless and intelligent shopping experience for Vietnamese customers.

## Features ✨

- 🧠 **Large Language Models (LLMs)**: Utilize state-of-the-art language models for natural conversations.
- 📚 **RAG (Retrieval Augmented Generation)**: Enhance responses with relevant product information from the database.
- 🛣️ **Semantic Router**: Intelligently direct queries to appropriate handling mechanisms.
- 🪞 **Reflection Module**: Improve response quality through context analysis and conversation history.
- 🇻🇳 **Vietnamese Language Support**: Tailored for the Vietnamese market and language.
- 🔍 **Advanced Product Search**: Case-insensitive and partial match product search capabilities.
- 💬 **Intelligent Chatbot Interface**: User-friendly chat interface for easy product queries and recommendations.

## Data Structure 🗂️

The product data is stored in MongoDB and includes the following fields:

- `product_code`: A unique identifier for each product (string)
- `product_name`: The name of the product (string)
- `material`: The material composition of the product (string)
- `size`: The size of the product (string)
- `color`: The color of the product (string)
- `brand`: The brand that manufactures or sells the product (string)
- `gender`: The target gender for the product (e.g., male, female, unisex) (string)
- `stock_quantity`: The quantity of the product available in stock (integer)
- `price`: The price of the product (numeric)
- `embedding`: Vector representation of the product for semantic search (array of floats)

## Installation 🛠️

To use ShoppingGPT, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/ShoppingGPT.git
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

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key
   ```

## Usage 🖥️

To start the ShoppingGPT assistant:

```bash
python main.py
```

## Technical Details 🔧

### Backend Architecture

ShoppingGPT uses a modular architecture:

1. **User Input** ➡️ **Semantic Router** 
2. **Semantic Router** ➡️ **RAG System** or **LLM** or **Human Support**
3. **RAG System** ➡️ **Response Generation**

#### Key Components

- **Semantic Router**: Uses embeddings to classify user queries and direct them to the appropriate handling mechanism.
- **RAG System**: Retrieves relevant product information from MongoDB to enhance the AI's responses.
- **LLM Integration**: Utilizes Google's Gemini model for generating human-like responses in Vietnamese.

### Directory Structure

- **`shoppinggpt/`**: Main package directory
  - **`router/`**: Contains the Semantic Router implementation
  - **`rag/`**: Implements the Retrieval Augmented Generation system
  - **`reflection/`**: Contains the Reflection module
  - **`embeddings/`**: Handles creation and management of embeddings
  - **`prompts/`**: Stores prompt templates for the LLM
  - **`utils/`**: Contains utility functions and helpers

## Feedback and Contributions 🌟

We welcome contributions! If you have any ideas, just open an issue and tell us what you think.

If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcome.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors 👨‍💻

ShoppingGPT is developed by [Your Name/Team]. If you have any questions, feel free to contact us or open an issue on GitHub.

## Acknowledgements 🙏

- OpenAI for GPT models
- Google for Gemini models
- MongoDB for vector search capabilities
- LangChain for providing excellent tools for building LLM applications

Thank you for using ShoppingGPT! We hope it enhances your e-commerce experience with AI-powered assistance. Happy shopping! 🛒✨