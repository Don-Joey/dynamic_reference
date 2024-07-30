import json
import ast
def write_output(filename, list_string):
    with open(filename, 'w') as file:
        json.dump(list_string,file,indent=4)
        #for string in list_string:
        #    file.write(string + '\n')

def read_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

def read_jsonl(filename):
    data_list = []
    # Open the JSONL file
    with open(filename, 'r') as file:
        for line in file:
            # Parse the JSON object from the line and append it to the list
            data_list.append(json.loads(line.strip()))
    return data_list

def prompt_to_chatml(prompt: str, start_token: str = "<|im_start|>", end_token: str = "<|im_end|>"):
        """Convert a text prompt to ChatML formal

        Examples
        --------
        >>> prompt = "<|im_start|>system\nYou are a helpful assistant.\n<|im_end|>\n<|im_start|>system
        name=example_user\nKnock knock.\n<|im_end|>\n<|im_start|>system name=example_assistant\nWho's
        there?\n<|im_end|>\n<|im_start|>user\nOrange.\n<|im_end|>"
        >>> print(prompt)
        <|im_start|>system
        You are a helpful assistant.
        <|im_end|>
        <|im_start|>system name=example_user
        Knock knock.
        <|im_end|>
        <|im_start|>system name=example_assistant
        Who's there?
        <|im_end|>
        <|im_start|>user
        Orange.
        <|im_end|>
        >>> prompt_to_chatml(prompt)
        [{'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': 'Knock knock.'},
        {'role': 'assistant', 'content': "Who's there?"},
        {'role': 'user', 'content': 'Orange.'}]
        """
        prompt = prompt.strip()
        assert prompt.startswith(start_token)
        assert prompt.endswith(end_token)

        def string_to_dict(to_convert):
            """Converts a string with equal signs to dictionary. E.g.
            >>> string_to_dict(" name=user university=stanford")
            {'name': 'user', 'university': 'stanford'}
            """
            return {s.split("=", 1)[0]: s.split("=", 1)[1] for s in to_convert.split(" ") if len(s) > 0}

        message = []
        for p in prompt.split("<|im_start|>")[1:]:
            newline_splitted = p.split("\n", 1)
            role = newline_splitted[0].strip()
            content = newline_splitted[1].split(end_token, 1)[0].strip()

            if role.startswith("system") and role != "system":
                # based on https://github.com/openai/openai-cookbook/blob/main/examples
                # /How_to_format_inputs_to_ChatGPT_models.ipynb
                # and https://github.com/openai/openai-python/blob/main/chatml.md it seems that system can specify a
                # dictionary of other args
                other_params = string_to_dict(role.split("system", 1)[-1])
                role = "system"
            else:
                other_params = dict()

            message.append(dict(content=content, role=role, **other_params))

        return message

def parse_formatted_text(text):
    # Remove the markdown-like code block delimiters
    cleaned_text = text.strip().strip('```python\n').strip('\n```')
    
    # Use ast.literal_eval to safely evaluate the string into a Python object
    parsed_data = ast.literal_eval(cleaned_text)
    
    return parsed_data