import openai
import os
import json
import time
from typing import List
from dotenv import load_dotenv
from schemas import MetricSchema
from article_scraping.scraping import scrape_news


def generate_metrics(articles_lst: List, verbose=False, return_values=True):
    load_dotenv()

    client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    with open('prompts/system_prompt_metrics.txt', 'r') as system_prompt_file:
        system_prompt = system_prompt_file.read()

    assistant = client.beta.assistants.create(
        model='gpt-4.1-mini',
        instructions=system_prompt,
        temperature=0.5,
        response_format={
            'type': 'json_schema',
            'json_schema':
                {
                    'name': 'MetricSchema',
                    'schema': MetricSchema.model_json_schema()
                }
        }
    )

    article_metric_pairs = []

    for article in articles_lst:
        thread = client.beta.threads.create(
            messages=[{
                'role': 'user',
                'content': json.dumps(article)
            }]
        )
        if verbose:
            print('created a thread, beginning query analysis')

        start_time = time.time()

        with client.beta.threads.runs.stream(
                thread_id=thread.id,
                assistant_id=assistant.id,
        ) as stream:
            stream.until_done()

        end_time = time.time()
        if verbose:
            print(f'Metric generation time: {end_time - start_time} seconds')

        messages = client.beta.threads.messages.list(thread_id=thread.id)

        result = messages.data[0].content[0].text.value

        article_metric_pairs.append((article, result))

    client.beta.assistants.delete(assistant_id=assistant.id)

    if return_values:
        return article_metric_pairs
    else:
        return None


if __name__ == '__main__':
    articles = scrape_news(verbose=True)
    articles_rated = generate_metrics(articles, verbose=True, return_values=True)
    print(articles_rated)
