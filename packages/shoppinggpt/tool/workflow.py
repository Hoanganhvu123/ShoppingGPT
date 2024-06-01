import requests
import pandas as pd 
import base64
import json
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor
from langchain.language_models.base import BaseLanguageModel
from langchain.outputparsers.OutputParserHelpers import formatResponse

class AirtableAgent:
    def __init__(self, base_id, table_id, api_key, model):
        self.base_id = base_id
        self.table_id = table_id
        self.api_key = api_key
        self.model = model

    def fetch_airtable_data(self, url, params):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def load_all(self):
        url = f"https://api.airtable.com/v0/{self.base_id}/{self.table_id}"
        params = {'pageSize': 100}
        all_records = []
        while True:
            data = self.fetch_airtable_data(url, params)
            all_records.extend(data.get('records', []))
            if 'offset' in data:
                params['offset'] = data['offset']
            else:
                break
        return [record['fields'] for record in all_records]

    def load_limit(self, limit):
        url = f"https://api.airtable.com/v0/{self.base_id}/{self.table_id}"
        params = {'maxRecords': limit}
        data = self.fetch_airtable_data(url, params)
        return [record['fields'] for record in data.get('records', [])]

    def process_data(self, data):
        # Placeholder method for processing data, this can be customized
        # to include any data processing logic needed.
        processed_data = []
        for record in data:
            processed_record = self.custom_processing(record)
            processed_data.append(processed_record)
        return processed_data

    def custom_processing(self, record):
        # Example of custom processing on each record
        # This method should be customized based on specific needs
        processed_record = {
            "name": record.get("Name", ""),
            "email": record.get("Email", ""),
            # Add more fields as needed
        }
        return processed_record

    def load_and_process_all(self):
        data = self.load_all()
        return self.process_data(data)

    def load_and_process_limit(self, limit):
        data = self.load_limit(limit)
        return self.process_data(data)

    async def run_python_code(self, code):
        # Use Pyodide to run Python code
        import pyodide
        pyodide.runPythonAsync(code)

    async def generate_python_code(self, dataframeColDict, input):
        # Generate Python code using the LLM
        chain = LLMChain({
            llm: self.model,
            prompt: PromptTemplate.fromTemplate(systemPrompt),
        })
        inputs = {
            "dict": dataframeColDict,
            "question": input
        }
        res = await chain.call(inputs)
        return res.text

    async def answer_query(self, input):
        data = self.load_all()
        json_data = json.dumps(data)
        base64_data = base64.b64encode(json_data.encode()).decode()
        
        code = f"""
            import pandas as pd
            import base64
            import json

            base64_string = "{base64_data}"

            decoded_data = base64.b64decode(base64_string)

            json_data = json.loads(decoded_data)

            df = pd.DataFrame(json_data)
            my_dict = df.dtypes.astype(str).to_dict()
            print(my_dict)
            json.dumps(my_dict)
        """
        dataframeColDict = await self.run_python_code(code)

        pythonCode = await self.generate_python_code(dataframeColDict, input)

        final_code = f"""
                import pandas as pd
                {pythonCode}
            """
        final_result = await self.run_python_code(final_code)

        final_chain = LLMChain({
            llm: self.model,
            prompt: PromptTemplate.fromTemplate(finalSystemPrompt),
        })
        final_inputs = {
            "question": input,
            "answer": final_result
        }
        result = await final_chain.call(final_inputs)
        return result.text


# Example usage:
# agent = AirtableAgent(base_id='your_base_id', table_id='your_table_id', api_key='your_api_key', model=your_llm_model)
# response = await agent.answer_query('Your question here')
# print(response)
