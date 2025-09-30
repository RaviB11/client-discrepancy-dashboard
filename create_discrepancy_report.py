import pandas as pd

# --- Configuration ---
SOURCE_FILE = 'source_client_data.csv'
TARGET_FILE = 'target_client_data.csv'
REPORT_FILE = 'discrepancy_report.csv'

def compare_datasets(source_df, target_df):
    """
    Compares source and target dataframes to identify discrepancies.
    This function mimics the logic of an advanced SQL query (like a FULL OUTER JOIN).
    """
    print("Comparing datasets to find discrepancies...")
    
    # Use an outer merge to find records in one table but not the other, and mismatches
    # The suffixes distinguish between columns from the source and target tables
    comparison_df = pd.merge(source_df, target_df, on='client_id', how='outer', suffixes=('_source', '_target'))

    discrepancies = []

    for index, row in comparison_df.iterrows():
        client_id = row['client_id']
        
        # Check for records missing in target
        if pd.isna(row['full_name_target']):
            discrepancies.append({
                'client_id': client_id,
                'discrepancy_type': 'Record Missing in Target',
                'field': 'N/A',
                'source_value': 'Record Exists',
                'target_value': 'NULL'
            })
            continue # Move to the next record

        # Check for records present only in target (new records)
        if pd.isna(row['full_name_source']):
            discrepancies.append({
                'client_id': client_id,
                'discrepancy_type': 'Record Missing in Source',
                'field': 'N/A',
                'source_value': 'NULL',
                'target_value': 'Record Exists'
            })
            continue # Move to the next record

        # For records present in both, check for field-level mismatches
        for col in source_df.columns:
            if col == 'client_id':
                continue # Skip the key used for joining
            
            source_val = row[f'{col}_source']
            target_val = row[f'{col}_target']
            
            # Use pandas' sophisticated NaN handling
            if pd.isna(source_val) and pd.isna(target_val):
                continue
            
            if source_val != target_val:
                discrepancies.append({
                    'client_id': client_id,
                    'discrepancy_type': 'Value Mismatch',
                    'field': col,
                    'source_value': source_val,
                    'target_value': target_val
                })
    
    if not discrepancies:
        print("No discrepancies found!")
        return pd.DataFrame()

    report_df = pd.DataFrame(discrepancies)
    print(f"Found {len(report_df)} total discrepancies.")
    return report_df

def main():
    """Main function to generate the discrepancy report."""
    print("--- Starting Discrepancy Analysis ---")
    try:
        source_df = pd.read_csv(SOURCE_FILE)
        target_df = pd.read_csv(TARGET_FILE)
    except FileNotFoundError as e:
        print(f"Error: {e}. Please run 'generate_mock_data.py' first.")
        return

    # Ensure data types are consistent for comparison, especially for dates
    source_df['registration_date'] = pd.to_datetime(source_df['registration_date'])
    target_df['registration_date'] = pd.to_datetime(target_df['registration_date'])
    
    report = compare_datasets(source_df, target_df)
    
    if not report.empty:
        report.to_csv(REPORT_FILE, index=False)
        print(f"Discrepancy report saved to {REPORT_FILE}")
        print("\nThis CSV file can now be connected to Tableau to create a dashboard.")
    
    print("--- Analysis Finished ---")

if __name__ == '__main__':
    main()
