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
    flag_pssr = False
    match technique:
        case TechniqueType.Primary_Direct:
            str_tf = 'pd'
        case TechniqueType.Secondary_Direct:
            str_tf = 'sc'
        case TechniqueType.PSSR:
            str_tf = 'sr'
            flag_pssr = True
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
    if flag_pssr:
        pssr_labels = {
            f'mon-conj-{str_tf}': [], 
            f'mon-maj-{str_tf}': []
        }
        data.update(pssr_labels)
    data.update({f'e-{str_tf}': []})

     
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        if flag_pssr:
            match = re.match(r"\['(.+), (\d+), opp-conj: (\d+), sqr-tri-sext: (\d+), major: (\d+), minor: (\d+), moon-opp-conj: (\d+), moon-sqr-tri-sext: (\d+), empty: (\d+)'\]", line)
        else:
            match = re.match(r"\['(.+), (\d+), opp-conj: (\d+), sqr-tri-sext: (\d+), major: (\d+), minor: (\d+), empty: (\d+)'\]", line)
        
        if match:
            time = match.group(1)
            count = int(match.group(2))
            opp_conj = int(match.group(3))
            sqr_tri_sext = int(match.group(4))
            major = int(match.group(5))
            minor = int(match.group(6))
            if flag_pssr:
                moon_opp_conj = int(match.group(7))
                moon_sqr_tri_sext = int(match.group(8))
                empty = int(match.group(9))
            else:
                empty = int(match.group(7))
            
            data['Time'].append(time)
            data[f'all-{str_tf}'].append(count)
            data[f'mj1-{str_tf}'].append(opp_conj)
            data[f'mj2-{str_tf}'].append(sqr_tri_sext)
            data[f'mja-{str_tf}'].append(major)
            data[f'min-{str_tf}'].append(minor)
            if flag_pssr:
                data[f'mon-conj-{str_tf}'].append(moon_opp_conj)
                data[f'mon-maj-{str_tf}'].append(moon_sqr_tri_sext)
            data[f'e-{str_tf}'].append(empty)
    
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
    file_list = ['9_14_ver1_1929-07-28_pssrCOUNT.txt', '9_14_ver1_1929-07-28_transitCOUNT.txt', '9_14_ver1_1929-07-28_secondariesCOUNT.txt']  
    final_df = load_and_concatenate_files(file_list)
    final_df_sorted = final_df.sort_values(by=['mon-conj-sr','mon-maj-sr'], ascending=[False, False])
  
    final_df_sorted.to_csv('9_14_ver1_sorted_planet_data.csv', index=False)
    #print(final_df.head())  

main()
