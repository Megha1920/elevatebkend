import requests
import re
import json
import logging
def extract_json(raw):
    try:
        
        cleaned_json = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', raw)
        cleaned_json = json.loads(cleaned_json)
        return cleaned_json
    except json.JSONDecodeError as e:
       
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
You are an assistant that generates multiple-choice questions based on a given context. Your task is to create a set of questions with one correct answer each.

Context:
--- start ---
{paragraph_context}
--- end ---

Output format:
The output should strictly be in JSON format, with each question, its corresponding options, and the correct answer enclosed in double quotes.

{{
"set": [
    {{
        "question": "Question 1",
        "options": [
            "Option 1",
            "Option 2",
            "Option 3",
            "Option 4"
        ],
        "correct_answer": " "
    }},
    {{
        "question": "Question 2",
        "options": [
            "Option 1",
            "Option 2",
            "Option 3",
            "Option 4"
        ],
        "correct_answer": " "
    }}
]
}}
"""





logging.basicConfig(level=logging.DEBUG)

def generate_questions(paragraph_context, num_questions):
    context_string = "\n".join(paragraph_context)

    questions_answers = []
    for i in range(num_questions):
        if i >= len(paragraph_context):
            logging.warning("Insufficient context paragraphs available.")
            break  # Break loop if we run out of context paragraphs

        prompt = prompt_template.format(paragraph_context=context_string)
        llm_output = llm_wrapper(prompt)
        extracted_output = extract_json(llm_output)

        if extracted_output and 'set' in extracted_output:
            questions_answers.extend(extracted_output["set"])  # Extend list with all generated questions
        else:
            # If extracted_output is None or 'set' is not present, log warning
            logging.warning("No questions generated for prompt: %s", prompt)
            continue

    # Return only the requested number of questions
    num_generated_questions = len(questions_answers)
    if num_generated_questions == 0:
        logging.error("No questions generated for given context and number of questions")
        return {}
    elif num_generated_questions < num_questions:
        logging.warning("Generated fewer questions than requested: %d out of %d", num_generated_questions, num_questions)
    return {"set": questions_answers[:num_questions]}