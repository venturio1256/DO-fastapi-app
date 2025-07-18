import json
import re
import yaml

def transform_json_to_yaml(input_file_path, output_file_path):
    # Read the file content
    with open(input_file_path, 'r') as file:
        file_content = file.read()

    # Split the file content into sections based on the comments
    sections = file_content.split('//')

    # Initialize a dictionary to hold the YAML data
    yaml_data = {}

    # Process each section
    for section in sections:
        # Extract the section title and content
        lines = section.strip().split('\n')
        if lines:
            section_title = lines[0].strip()
            json_content = '\n'.join(lines[1:])

            # Use regular expression to find all JSON objects in the section content
            json_objects_in_section = re.findall(r'{(?:[^{}]|{(?:[^{}]|{(?:[^{}]|{[^{}]*})*})*})*}', json_content)

            # Parse each JSON object and convert to YAML
            parsed_objects = [json.loads(obj) for obj in json_objects_in_section]
            if parsed_objects:
                yaml_data[section_title] = yaml.dump(parsed_objects, sort_keys=False)

    # Write the YAML data to the output file
    with open(output_file_path, 'w') as yaml_file:
        for section_title, yaml_content in yaml_data.items():
            yaml_file.write(f"{section_title}: |\n{yaml_content}\n\n")

# Specify the input and output file paths
#input_file_path = 'path_to_your_input_file.json'
#output_file_path = 'transformed_data.yaml'

# Call the function to transform the JSON file to YAML
#transform_json_to_yaml(input_file_path, output_file_path)
if __name__ == "__main__":
    # Example usage
    input_file_path = 'WhatzonTV_Sports_JSON.json'
    output_file_path = 'transformed_data.yaml'
    transform_json_to_yaml(input_file_path, output_file_path)