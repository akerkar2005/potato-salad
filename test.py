import modal
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from openai import OpenAI

# Create the modal app
app = modal.App("test", image=modal.Image.debian_slim().pip_install("openai", "fastapi"))

# Define the function that will interact with OpenAI
@app.function(secrets=[modal.Secret.from_name("openai-secret")])
def complete_text(prompt: str):
    client = OpenAI()

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content


# Define the FastAPI app for the API endpoints
@app.local_entrypoint()
def create_backend():
    fastapi_app = FastAPI()

    @fastapi_app.post("/complete")
    async def complete_text_endpoint(prompt: str):
        # Call the Modal function to generate a response
        completion = await complete_text.remote(prompt)
        return JSONResponse({"response": completion})

    return fastapi_app

