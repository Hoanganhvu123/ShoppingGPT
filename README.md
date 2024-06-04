# ShoppingGPT 🛒🤖

ShoppingGPT is an intelligent shopping assistant designed to help users query product data stored in a CSV file. This project leverages the power of Python, Pandas, and an advanced LLM (Language Learning Model) to provide detailed information about various products.

## Features ✨

- 🔍 **Product Information Retrieval:** Retrieve detailed information about products based on user queries.
- 🔤 **Case-Insensitive Search:** Handle product names in a case-insensitive manner and allow for partial matches.
- ⚡ **Efficient Data Processing:** Utilize efficient indexing and filtering techniques to process data.
- 🔄 **Data Conversion:** Convert string values to float for the 'price' column if necessary.
- 🛡️ **Error Handling:** Validate input to prevent potential errors.

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

1. Clone the repository:
    ```bash
    git clone https://github.com/Hoanganhvu123/ShoppingGPT.git
    cd ShoppingGPT
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage 🚀

To start using ShoppingGPT, you need to have your product data in a CSV file. Here is an example of how to run the script:

```python
import pandas as pd
from your_module import create_product_manager_chain, ChatGroq

# Load your product data
df = pd.read_csv('path/to/your/product_data.csv')

# Initialize the LLM
llm = ChatGroq(...)

# Create the product manager chain
chain = create_product_manager_chain(llm, df)

# Example query
query = "Find details about a specific product"
result = chain.invoke({"input": query})
print(result)

