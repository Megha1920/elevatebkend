import requests
import re
import json

def extract_json(raw):
    try:
        
        cleaned_json = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', raw)
        cleaned_json = json.loads(cleaned_json)
        return cleaned_json
    except json.JSONDecodeError as e:
        print(f"Error loading JSON: {e}")
        return None


def llm_wrapper(prompt):
    output_string = ""

    endpoint = 'https://api.together.xyz/inference'
    api_key = "1b871825a85dd89cb5350cae96dba2a09059cbef143ca9dfa26e2280c7dcab8c"

    response = requests.post(
        url=endpoint,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "prompt": f"[INST] {prompt} [/INST]",
            "max_tokens": 16000,
            "temperature": 0.2,
        })

    if response.status_code == 200:
        content = response.text
         
        content_json = response.json()
        output_string = content_json["output"]["choices"][0]["text"]
    else:
        raise Exception(f"Request failed with status code {response.status_code}")

    return output_string




prompt_template = """

You are a expert question setter for examinations. You try to consume the context given to you and formulate long answer questions based on that and answer them.
Long answer questions are questions that require a detailed explanation of the answer. The answers must be 300-500 words in length.
You are to generate 5 such pairs of questions and answers

Context:
--- start ---
{paragraph_context}
--- end ---

Output format:
The output should stricly be in json format

{{
"set": [
    {{
        "question": "Question 1",
        "answer": "Answer 1"
    }},
    {{
        "question": "Question 2",
        "answer": "Answer 2"
    }},
    {{
        "question": "Question 3",
        "answer": "Answer 3"
    }},
    {{
        "question": "Question 4",
        "answer": "Answer 4"
    }},
    {{
        "question": "Question 5",
        "answer": "Answer 5"
    }}
    {{
        "question": "Question 6",
        "answer": "Answer 6"
    }}
]
}}
"""



def generate_questions(paragraph_context, num_questions): 
    context_string = "\n".join(paragraph_context)

    questions_answers = []
    for i in range(num_questions):
        if i >= len(paragraph_context):
            break  # Break loop if we run out of context paragraphs
        prompt = prompt_template.format(paragraph_context=context_string)
        llm_output = llm_wrapper(prompt)
        extracted_output = extract_json(llm_output)
        if extracted_output and 'set' in extracted_output:
            questions_answers.extend(extracted_output["set"])  # Extend list with all generated questions
        else:
            # If extracted_output is None or 'set' is not present, skip this iteration
            continue

    return {"set": questions_answers[:num_questions]}  # Return only the requested number of questions

 



