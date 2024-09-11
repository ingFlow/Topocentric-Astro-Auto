import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class TechniqueType:
    Primary_Direct = 0
    Secondary_Direct = 1
    PSSR = 2
    Transit = 3

def extract_data_from_file(filename, technique: TechniqueType):
    str_tf = '?'
    match technique:
        case TechniqueType.Primary_Direct:
            str_tf = 'pd'
        case TechniqueType.Secondary_Direct:
            str_tf = 'sc'
        case TechniqueType.PSSR:
            str_tf = 'sr'
        case TechniqueType.Transit:
            str_tf = 'tr'
       
    data = {
        'Time': [],
        f'all-{str_tf}': [],
        f'mj1-{str_tf}': [],
        f'mj2-{str_tf}': [],
        f'mja-{str_tf}': [],
        f'min-{str_tf}': []
    }
    
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        match = re.match(r"\['(.+), (\d+), opp/conj: (\d+)', 'sqr/tri/sext: (\d+)', 'major: (\d+)', 'minor: (\d+)'\]", line)
        
        if match:
            time = match.group(1)
            count = int(match.group(2))
            opp_conj = int(match.group(3))
            sqr_tri_sext = int(match.group(4))
            major = int(match.group(5))
            minor = int(match.group(6))
            
            data['Time'].append(time)
            data[f'all-{str_tf}'].append(count)
            data[f'mj1-{str_tf}'].append(opp_conj)
            data[f'mj2-{str_tf}'].append(sqr_tri_sext)
            data[f'mja-{str_tf}'].append(major)
            data[f'min-{str_tf}'].append(minor)
    
    df = pd.DataFrame(data)
    
    return df

def load_and_concatenate_files(file_list):
    """Load multiple text files and concatenate them into a single DataFrame."""
    all_dfs = []
    
    for filename in file_list:
        technique = -1
        if 'pssr' in filename:
            technique = TechniqueType.PSSR
        elif 'primar' in filename:
            technique = TechniqueType.Primary_Direct
        elif 'second' in filename:
            technique = TechniqueType.Secondary_Direct
        elif 'trans' in filename:
            technique = TechniqueType.Transit 

        df = extract_data_from_file(filename, technique)
        all_dfs.append(df)
    
    final_df = all_dfs[0]
    for df in all_dfs[1:]:
        final_df = pd.merge(final_df, df, on='Time')
    
    return final_df

def count_all_col(csv_filename):
    df = pd.read_csv(csv_filename)

    columns_with_all = [col for col in df.columns if 'all' in col.lower()]
    df['cumulative_all'] = df[columns_with_all].sum(axis=1)
    df = df.sort_values(by=['cumulative_all'], ascending=[False])

    df.to_csv(csv_filename, index=False)
    print(df.head())  # Print the first few rows to verify


def count_all_major(csv_filename):
    df = pd.read_csv(csv_filename)

    columns_with_all = [col for col in df.columns if 'mja' in col.lower()]
    df['count_mja'] = df[columns_with_all].sum(axis=1)
    df = df.sort_values(by=['count_mja'], ascending=[False])

    df.to_csv(csv_filename, index=False)
    print(df.head())  # Print the first few rows to verify


def count_all_major_opp(csv_filename):
    df = pd.read_csv(csv_filename)

    columns_with_all = [col for col in df.columns if 'mj1' in col.lower()]
    df['count_mj1'] = df[columns_with_all].sum(axis=1)
    df = df.sort_values(by=['count_mj1'], ascending=[False])

    df.to_csv(csv_filename, index=False)
    print(df.head())  # Print the first few rows to verify

def main():
    file_list = ['9_9_ 1940-10-09_primariesCOUNT.txt', '9_9_ 1940-10-09_secondariesCOUNT.txt']  
    final_df = load_and_concatenate_files(file_list)
    final_df_sorted = final_df.sort_values(by=['mja-pd','mja-sc'], ascending=[False,False])
   
    final_df_sorted.to_csv('9_9_ver2_sorted_planet_data.csv', index=False)
    #print(final_df.head())  

main()
count_all_col('9_9_ver2_sorted_planet_data.csv')
count_all_major_opp('9_9_ver2_sorted_planet_data.csv')
count_all_major('9_9_ver2_sorted_planet_data.csv')
