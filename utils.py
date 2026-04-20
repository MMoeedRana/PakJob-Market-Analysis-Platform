import pandas as pd
import re

def clean_data(df):
    # 1. Remove duplicates
    df = df.drop_duplicates()

    # 2. Extract numeric salary (Average of range)
    def parse_salary(val):
        nums = re.findall(r'\d+', val.replace(',', ''))
        if len(nums) >= 2:
            return (int(nums[0]) + int(nums[1])) / 2
        elif len(nums) == 1:
            return int(nums[0])
        return None

    df['Salary_Numeric'] = df['Salary'].apply(parse_salary)
    
    # 3. Standardize Cities (e.g., "Lahore (On-site)" -> "Lahore")
    df['City'] = df['Location'].apply(lambda x: x.split('(')[0].strip())
    
    return df