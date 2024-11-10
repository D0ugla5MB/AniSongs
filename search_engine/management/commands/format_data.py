import warnings
import os

req_files = ['mal_data.csv', 'spotify_data.csv']

for file in req_files:
    if not os.path.exists(file):
        warnings.warn(
            f"Required file '{file}' is missing. Please create or add this file before running the script.",
            UserWarning
        )