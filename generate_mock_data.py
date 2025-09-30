import pandas as pd
from faker import Faker
import random
import numpy as np

# --- Configuration ---
NUM_RECORDS = 1000
SOURCE_FILE = 'source_client_data.csv'
TARGET_FILE = 'target_client_data.csv'
DISCREPANCY_RATE = 0.1 # 10% of records will have some form of issue

fake = Faker()

def create_source_data():
    """Generates the pre-migration (source) dataset."""
    print(f"Generating {NUM_RECORDS} source records...")
    data = {
        'client_id': [100 + i for i in range(NUM_RECORDS)],
        'full_name': [fake.name() for _ in range(NUM_RECORDS)],
        'email': [fake.email() for _ in range(NUM_RECORDS)],
        'phone_number': [fake.phone_number() for _ in range(NUM_RECORDS)],
        'account_status': [random.choice(['Active', 'Inactive', 'Pending Review']) for _ in range(NUM_RECORDS)],
        'registration_date': [fake.date_between(start_date='-5y', end_date='today') for _ in range(NUM_RECORDS)],
        'lifetime_value': [round(random.uniform(100, 5000), 2) for _ in range(NUM_RECORDS)],
    }
    df = pd.DataFrame(data)
    df.to_csv(SOURCE_FILE, index=False)
    print(f"Source data saved to {SOURCE_FILE}")
    return df

def create_target_data(source_df):
    """Generates the post-migration (target) dataset with induced discrepancies."""
    print("Generating target data with discrepancies...")
    target_df = source_df.copy()
    
    num_discrepancies = int(NUM_RECORDS * DISCREPANCY_RATE)
    records_to_modify = random.sample(range(NUM_RECORDS), num_discrepancies)

    for idx in records_to_modify:
        # Pick a random type of error to introduce
        error_type = random.choice(['value_mismatch', 'missing_record', 'format_change', 'corruption'])

        if error_type == 'value_mismatch' and idx < len(target_df):
            # Change account status
            original_status = target_df.at[idx, 'account_status']
            possible_statuses = ['Active', 'Inactive', 'Pending Review']
            possible_statuses.remove(original_status)
            target_df.at[idx, 'account_status'] = random.choice(possible_statuses)

        elif error_type == 'missing_record':
            # Drop a record completely
            target_df.drop(index=idx, inplace=True)

        elif error_type == 'format_change' and idx < len(target_df):
            # Change phone number format
            target_df.at[idx, 'phone_number'] = f"({fake.msisdn()[:3]}) {fake.msisdn()[3:6]}-{fake.msisdn()[6:10]}"
        
        elif error_type == 'corruption' and idx < len(target_df):
            # Corrupt an email address
            email = target_df.at[idx, 'email']
            target_df.at[idx, 'email'] = email.replace('@', '_at_')


    # Introduce some completely new records that weren't in the source
    num_new_records = int(num_discrepancies / 4)
    new_records = []
    for i in range(num_new_records):
         new_records.append({
            'client_id': NUM_RECORDS + 100 + i,
            'full_name': fake.name(),
            'email': fake.email(),
            'phone_number': fake.phone_number(),
            'account_status': 'Active',
            'registration_date': fake.date_this_year(),
            'lifetime_value': round(random.uniform(100, 5000), 2)
        })
    
    target_df = pd.concat([target_df, pd.DataFrame(new_records)], ignore_index=True)

    target_df.to_csv(TARGET_FILE, index=False)
    print(f"Target data saved to {TARGET_FILE}")
    return target_df


if __name__ == '__main__':
    source_data = create_source_data()
    create_target_data(source_data)
    print("\nMock data generation complete.")
    print(f"Run 'python create_discrepancy_report.py' to generate the analysis.")
