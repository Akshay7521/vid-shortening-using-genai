import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import asyncio
import json

load_dotenv()

# Initialize the Azure OpenAI model
def setup_azure_openai():
    endpoint = os.getenv("ENDPOINT_URL")
    deployment = os.getenv("DEPLOYMENT_NAME")
    subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

    return AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=subscription_key,
        api_version=os.getenv("AZURE_OPENAI_VERSION")
    ), deployment

client, deployment = setup_azure_openai()

async def invoke_genai_model(prompt):
    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant that summarizes transcripts and provides important timestamps."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    
    completion = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_tokens=3000,
        temperature=0,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )
    
    response = completion.choices[0].message.content
    print("Response:", response)
    return response

async def shorten_transcript(transcript: str, timestamps: list):
    # Split the transcript into smaller chunks
    max_length = 10000  # Adjust this value based on the token limit
    print("Transcript Length:", len(transcript))
    chunks = [transcript[i:i + max_length] for i in range(0, len(transcript), max_length)]
    print("Number of chunks:", len(chunks))
    important_timestamps = []
    
    # Concatenate all chunks into a single prompt
    concatenated_transcript = " ".join(chunks)
    prompt = f"Analyze the following video transcript and provide a JSON object of start and end times for the important and meaningful content only. Give a score out of ten to each chunk based on the importance of content and return only the high scoring and important chunks' start and end times in ascending order of time in a JSON object. The object should contain only the important timestamps with start and end times where the speaker is speaking something important. Summarize the content to a maximum of 20 percent of the actual length or time, not more than that. The maximum summary video length should not be more than 10 minutes. We will create short clips from this transcript which will have important content only:\n\n{concatenated_transcript}\n\nTimestamps:\n{timestamps}"
    
    response = await invoke_genai_model(prompt)
    
    # Extract JSON object from response
    json_start = response.find('[')
    json_end = response.rfind(']') + 1

    if json_start == -1 or json_end == 0:
        raise ValueError("No valid JSON found in response")
    
    json_response = response[json_start:json_end]
    print("json_object:", json_response)
    
    # Extract important timestamps from the summary
    try:
        important_chunks = json.loads(json_response)
        for chunk in important_chunks:
            start_time = chunk['start']
            end_time = chunk['end']
            important_timestamps.append({'start': start_time, 'end': end_time})
    except json.JSONDecodeError:
        print("Failed to decode JSON from response")
    
    # Print important_timestamps array 
    print("Important Timestamps:", important_timestamps)
    return important_timestamps