import openai
import json
import time
import tiktoken
import os
from dotenv import load_dotenv


def message_llm(article: dict,
                client: openai.OpenAI,
                assistant,
                verbose=False):

    encoding = tiktoken.encoding_for_model('gpt-4o-mini')
    num_tokens = len(encoding.encode(json.dumps(article)))
    if verbose:
        print('created a thread, beginning query analysis')
        print(f'Token length: {num_tokens}')
        start_time = time.time()

    thread = client.beta.threads.create(
        messages=[{
            "role": "user",
            "content": json.dumps(article),
        }]
    )

    with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
    ) as stream:
        stream.until_done()

    if verbose:
        end_time = time.time()
        print(f'Metric generation time: {end_time - start_time} seconds')

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    result = messages.data[0].content[0].text.value
    client.beta.threads.delete(thread_id=thread.id)

    return json.loads(result)


def delete_all_assistants(client: openai.OpenAI):
    while True:
        assistants = json.loads(client.beta.assistants.list().model_dump_json())['data']
        if assistants:
            return
        for assistant in assistants:
            print(assistant)
            try:
                client.beta.assistants.delete(assistant_id=assistant['id'])
            except:
                return


if __name__ == '__main__':
    load_dotenv()
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    delete_all_assistants(client)
