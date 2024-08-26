"""
Finds errors in a log file and processes them using an external API.

The `find_errors_in_log_file()` function reads a log file specified as a command-line argument,
searches for lines containing error-related keywords, and extracts the surrounding context
(a configurable number of lines before and after the error line). The extracted error logs
are returned as a list.

The `process_error_logs()` function takes the list of error logs and sends them to an external
API for further processing. The API response is then printed to the console.
"""

import sys
import requests
import json
import os
from collections import defaultdict


## # # # # # # # #
# Config section #
## # # # # # # # # 
prelines = 10
postlines = 10

# API endpoint for the external API
ollama_api_url = "http://ollama.dc.int:11434/api/generate"

#model to use for analysis
model = "pki/logpt"





# keywords to search for in the log file
error_keywords = {
    "error": "Error",
    "warning": "Warning",
    "critical": "Critical",
    "exception": "Exception"
}



def find_errors_in_log_file():
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <filename>")
        return None

    log_file_path = sys.argv[1]
    if not os.path.exists(log_file_path):
        print(f"Error: File '{log_file_path}' not found.")
        return None

    try:
        error_logs = []
        keyword_set = set(error_keywords.keys())
        
        with open(log_file_path, 'r') as log_file:
            lines = log_file.readlines()
            line_count = len(lines)
            error_indices = defaultdict(list)

            for i, line in enumerate(lines):
                lower_line = line.lower()
                for keyword in keyword_set:
                    if keyword in lower_line:
                        error_indices[keyword].append(i)
                        break

            for keyword, indices in error_indices.items():
                log_type = error_keywords[keyword]
                for index in indices:
                    start_index = max(0, index - prelines)
                    end_index = min(line_count, index + postlines + 1)
                    error_logs.extend([f"{log_type}: {lines[i]}" for i in range(start_index, end_index)])

        return error_logs
    except IOError as e:
        print(f"Error reading file: {e}")
        return None

def process_error_logs(error_logs):
    if not error_logs:
        print("No errors found or unable to process log file.")
        return

    data = {
        "prompt": "\n".join(error_logs),
        "model": model
    }

    try:
        with requests.post(ollama_api_url, json=data, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    try:
                        json_data = json.loads(line)
                        if not json_data['done']:
                            print(json_data['response'], end='')
                        else:
                            break
                    except json.JSONDecodeError:
                        print("Error: Invalid JSON response")
    except requests.RequestException as e:
        print(f"Error making API request: {e}")

if __name__ == "__main__":
    error_logs = find_errors_in_log_file()
    process_error_logs(error_logs)
