import os
import shutil
import logging
from datetime import datetime
import time
import requests

# Set up logging
logging.basicConfig(
    filename='./logs/etl.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# API endpoint for CSV upload
#local API_ENDPOINT='http://localhost:5000/upload_csv'
API_ENDPOINT = 'http://54.174.85.3:5000/upload_csv'
BATCH_SIZE = 10
# Directories
input_dir = './input'
processed_dir = './input/processed'
errors_dir = './input/errors'

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
    pattern = ['departments.csv', 'jobs.csv', 'hired_employees.csv']
    priority = {val: i for i, val in enumerate(pattern)}
    return sorted(arr, key=lambda x: priority.get(x.split('_')[0], float('inf')))

files = custom_sort(files)
print('Files to process:',files)
print('\t')

for file in files:
    start_time = time.time()
    file_path = os.path.join(input_dir, file)
    
    # Determine table based on file name
    table_name = file.split('.')[0].lower()
    if(table_name=='hired_employees'):
        table_name='employees'
    batch_size = BATCH_SIZE

    try:
        # Upload file to API
        with open(file_path, 'rb') as f:
            response = requests.post(f'{API_ENDPOINT}?table={table_name}&batch_size={batch_size}', files={'file': f})
        if response.status_code == 200:
            # Analize API response stats
            api_stats = response.json()
            if "_error_row_count" in api_stats and api_stats['_error_row_count']!=0:
                # File with errors processed by API, move to errors directory
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                new_filename = f"{file.split('.')[0]}_{timestamp}.csv"
                shutil.move(file_path, os.path.join(errors_dir, new_filename))
                print('========================================================================')
                print(f'File {file} processed with errors')
                print('------------------------------------------------------------------------')
                print('Total rows processed:',api_stats['_total_rows'])
                print('Rows inserted:',api_stats['_inserted_rows'])
                print('Rows with errors:',api_stats['_error_row_count'])
                print(api_stats['_message'])
                logging.info(f'File {file} processed with errors, please review logs')
                logging.info(api_stats)
                error_count += 1
            else:
                # File successfully processed by API, move to processed directory
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                new_filename = f"{file.split('.')[0]}_{timestamp}.csv"
                shutil.move(file_path, os.path.join(processed_dir, new_filename))
                print('========================================================================')
                print(f'File {file} processed successfully')
                print('------------------------------------------------------------------------')
                print('Total rows processed:',api_stats['_total_rows'])
                print('Rows inserted:',api_stats['_inserted_rows'])
                print(api_stats['_message'])
                success_count += 1
                logging.info(f'File {file} processed successfully')
                logging.info(api_stats)
        else:
            # API returned an error, move to errors directory
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            new_filename = f"{file.split('.')[0]}_{timestamp}.csv"
            shutil.move(file_path, os.path.join(errors_dir, new_filename))
            print('========================================================================')
            print(f'Error processing file {file}: {response.json()}')
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
    print(f'Processing time for file {file}: {duration:.2f} seconds')
    print('\t')
    logging.info(f'Processing time for file {file}: {duration:.2f} seconds')

# Print execution result
print('------------------------------------------------------------------------')
print(f'Successful files processed: {success_count}')
print(f'Files with errors: {error_count}')