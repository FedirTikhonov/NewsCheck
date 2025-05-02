import openai
import json
import time
import tiktoken


def generate_metric(article: dict,
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


def find_same_issue_articles_with_llm(client: openai.OpenAI,
                                      assistant,
                                      request_body: dict):
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": json.dumps(request_body),
            }
        ]
    )

    with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
    ) as stream:
        stream.until_done()

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    result = messages.data[0].content[0].text.value
    client.beta.threads.delete(thread_id=thread.id)

    return json.loads(result)['ids']


def categorize_article(request_body: dict, client: openai.OpenAI, assistant):
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": json.dumps(request_body),
            }
        ]
    )

    with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
    ) as stream:
        stream.until_done()

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    result = messages.data[0].content[0].text.value
    client.beta.threads.delete(thread_id=thread.id)

    return json.loads(result)['category']




