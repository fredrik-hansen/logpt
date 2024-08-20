import sys
import requests
import json
import os

# prelines and postlines represent the number of lines of context to include in the output around the error
prelines = 10
postlines = 10

def find_errors_in_log_file():
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <filename>")
        return None

    log_file_path = sys.argv[1]
    if not os.path.exists(log_file_path):
        print(f"Error: File '{log_file_path}' not found.")
        return None

    try:
        with open(log_file_path, 'r') as log_file:
            log_lines = log_file.readlines()

        error_logs = []
        for i, line in enumerate(log_lines):
            if "error" in line.lower():
                start_index = max(0, i - prelines)
                end_index = min(len(log_lines), i + postlines + 1)
                error_logs.extend(log_lines[start_index:end_index])

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
        "model": "pki/logpt"
    }

    try:
        response = requests.post("http://ollama.dc.int:11434/api/generate", json=data, stream=True)
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                try:
                    json_data = json.loads(line)
                    if json_data['done'] == False:
                        print(json_data['response'], end='')
                    else:
                        break
                except json.JSONDecodeError:
                    print("Error: Invalid JSON response")
    except requests.RequestException as e:
        print(f"Error making API request: {e}")
    finally:
        response.close()

if __name__ == "__main__":
    error_logs = find_errors_in_log_file()
    process_error_logs(error_logs)