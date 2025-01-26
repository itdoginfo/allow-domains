#!/usr/bin/python3.10

import json
import os
import subprocess

directories = ['Categories', 'Services']

output_directory = 'JSON'
os.makedirs(output_directory, exist_ok=True)
compiled_output_directory = 'SRS'
os.makedirs(compiled_output_directory, exist_ok=True)

for directory in directories:
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path):
            domains = []
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    domain = line.strip()
                    if domain:
                        domains.append(domain)

        data = {
            "version": 2,
            "rules": [
                {
                    "domain_suffix": domains
                }
            ]
        }

        output_file_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.json")

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(data, output_file, indent=4)

        print(f"JSON file generated: {output_file_path}")

print("\nCompile JSON files to .srs files...")
for filename in os.listdir(output_directory):
    if filename.endswith('.json'):
        json_file_path = os.path.join(output_directory, filename)
        srs_file_path = os.path.join(compiled_output_directory, f"{os.path.splitext(filename)[0]}.srs")
        try:
            subprocess.run(
                ["sing-box", "rule-set", "compile", json_file_path, "-o", srs_file_path], check=True
            )
            print(f"Compiled .srs file: {srs_file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Compile error {json_file_path}: {e}")