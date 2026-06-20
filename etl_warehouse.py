import pandas as pd 
import logging
import os
logging.basicConfig(filename = 'etl.log',
                    level = logging.INFO,
                    format= " %(asctime)s %(levelname)s %(message)s ")
def extract(filename):
    try:
        df=pd.read_csv(filename)

        logging.info(f'Extracted {filename}')
        return df

    except FileNotFoundError:
        print(f'{filename} not found')
        return None
def transform(df):
    if df is None:
        return None
    before = len(df)

    df=df.drop_duplicates()

    after = len(df)
    logging.info(f'Removed {before-after} duplicate rows')
    return df
def validate(df,filename):
    if df is None:
        return False
        
    if df.empty:
        print(f'{filename} is empty!')
        return False
        
    return True
    
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
    logging.info(f"Warehouse created with {len(full_df)}")
    return full_df
    
