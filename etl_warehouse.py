import pandas as pd

def extract(filename):
    """Extract data from CSV files using pandas.
    
    Args:
        filename: Path to CSV file
        
    Returns:
        DataFrame with loaded data, or None if file not found
    """
    try:
        df = pd.read_csv(filename)
        print(f'[SUCCESS] {filename}: {len(df)} rows, {len(df.columns)} columns')
        return df
    
    except FileNotFoundError:
        print(f'[ERROR] {filename} not found')
        return None


def transform(df):
    """Transform and clean sales data.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    if df is None:
        return None
    
    # Data validation and cleaning
    df = df.dropna()
    df = df.drop_duplicates()
    
    print(f'[TRANSFORM] Data cleaned: {len(df)} valid records')
    return df


def load(df, table_name):
    """Load transformed data into PostgreSQL warehouse.
    
    Args:
        df: DataFrame to load
        table_name: Target table name in database
    """
    if df is None:
        return False
    
    print(f'[LOAD] Loading {len(df)} records into {table_name}...')
    # PostgreSQL loading logic (coming in Phase 2)
    return True


def main():
    """Execute complete ETL pipeline for sales data warehouse."""
    # Extract
    sales_data = extract(r"C:\Users\ss\.vscode\products.csv")
    
    # Transform
    clean_data = transform(sales_data)
    
    # Load (coming soon)
    # load(clean_data, 'sales_fact')
    
    print('[PIPELINE] ETL process complete!')


if __name__ == '__main__':
    main()
