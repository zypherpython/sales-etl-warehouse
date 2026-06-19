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
    if df is None:
        return None
    df=df.drop_duplicates()
    return df

def build_warehouse(customer_df,products_df,orders_df):
    order_productdf = orders_df.merge(
        products_df,
        on = "product_id"
          
    )
    full_df= order_productdf.merge(
        customer_df,
        on = 'customer_id'
    )
    full_df['revenue'] = ( full_df['quantity'] * full_df['price'])
    return full_df
