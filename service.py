from . import model

from pydantic import BaseModel
from langchain.prompts import PromptTemplate

# Define the configuration model for inputs
class InputModel(BaseModel):
    user_name: str
    bot_name: str
    memory: str
    chat_history: str
    input_text: str

# Example usage of model.CustomModelLLM and model.CustomModelConfig
config = model.CustomModelConfig(
    api_url="https://guanaco-submitter.chai-research.com/endpoints/onsite/chat",
    api_key="CR_6700b8e747434541924772becb8fa85a"
)
model_instance = model.CustomModelLLM(config=config)

# Define the prompt template
prompt_template = PromptTemplate(
    input_variables=["user_name", "bot_name", "memory", "chat_history", "input_text"],
    template=(
        "Memory: {memory}\n"
        "Chat history:\n{chat_history}\n"
        "{user_name}: {input_text}\n"
        "{bot_name}:"
    )
)

# Function to run the sequence manually
def run_sequence(inputs):
    # Validate inputs using InputModel
    input_data = InputModel(**inputs)
    # Format the prompt using the template
    prompt = prompt_template.format(**input_data.dict())
    # Call the model with the formatted prompt
    response = model_instance._call(prompt)
    return {"response": response}
