import os
import shutil
import logging
from datetime import datetime
import time
from dotenv import load_dotenv
import requests




# Load environment variables from .env file
load_dotenv(dotenv_path='../.env')

# Set up logging
logging.basicConfig(
    filename='./etl/logs/etl.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# API endpoint for CSV upload
#API_ENDPOINT = os.getenv('API_ENDPOINT')
API_ENDPOINT='http://localhost:5000/upload_csv'

# Directories
input_dir = './etl/input'
processed_dir = './etl/input/processed'
errors_dir = './etl/input/errors'

# Create directories if they don't exist
os.makedirs(input_dir, exist_ok=True)
os.makedirs(processed_dir, exist_ok=True)
os.makedirs(errors_dir, exist_ok=True)


# Get list of CSV files in input directory
files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]

success_count = 0
error_count = 0

# To execute in order departments, jobs, hired_employees
def custom_sort(arr):
    pattern = ['departments', 'jobs', 'hired_employees']
    priority = {val: i for i, val in enumerate(pattern)}
    return sorted(arr, key=lambda x: priority.get(x.split('_')[0], float('inf')))

files = custom_sort(files)

for file in files:
    start_time = time.time()
    file_path = os.path.join(input_dir, file)
    
    # Determine table based on file name
    table_name = file.split('.')[0].lower()
    if(table_name=='hired_employees'):
        table_name='employees'
    batch_size = 10

    try:
        # Upload file to API
        with open(file_path, 'rb') as f:
            response = requests.post(f'{API_ENDPOINT}?table={table_name}&batch_size={batch_size}', files={'file': f})
        if response.status_code == 200:
            # Analize API response stats
            api_stats = response.json()
            print(api_stats)
            if api_stats['_error_row_count']!=0:
                # File with errors processed by API, move to errors directory
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                new_filename = f"{file.split('.')[0]}_{timestamp}.csv"
                shutil.move(file_path, os.path.join(errors_dir, new_filename))
                logging.info(f'File {file} processed with errors, please review logs')
                logging.info(api_stats)
                error_count += 1
            else:
                # File successfully processed by API, move to processed directory
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                new_filename = f"{file.split('.')[0]}_{timestamp}.csv"
                shutil.move(file_path, os.path.join(processed_dir, new_filename))
                logging.info(f'File {file} processed successfully')
                logging.info(api_stats)
                success_count += 1
        else:
            # API returned an error, move to errors directory
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            new_filename = f"{file.split('.')[0]}_{timestamp}.csv"
            shutil.move(file_path, os.path.join(errors_dir, new_filename))
            logging.error(f'Error processing file {file}: {response.json()}')
            error_count += 1
    except Exception as e:
        # Exception occurred, move to errors directory
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        new_filename = f"{file.split('.')[0]}_{timestamp}.csv"
        shutil.move(file_path, os.path.join(errors_dir, new_filename))
        logging.error(f'Error processing file {file}: {str(e)}')
        error_count += 1
    
    duration = time.time() - start_time
    logging.info(f'Processing time for file {file}: {duration:.2f} seconds')

# Print execution result
print(f'Successful files processed: {success_count}')
print(f'Files with errors: {error_count}')


def main():
        csv_dataframes=extract_etl()
        load_etl(csv_dataframes)
        transform_etl()

if __name__ == "__main__":
    main()