"""
batch/analysis.py - kept fully per your decision (see the migration
plan), not deleted despite having zero current callers anywhere in the
application. Post-processes COUNT.txt files (extract_data_from_file,
load_and_concatenate_files) into merged CSVs/plots for manual
rectification-candidate review.

Recent change (de-duplication/mechanical-move phases): this file's own
local TechniqueType enum (Primary_Direct/Secondary_Direct/PSSR/Transit -
note the different casing from the canonical enum) has been replaced with
a direct import of core.constants.aTechniqueType, with every usage site
updated to the canonical casing (PRIMARY_DIRECT, SECONDARY_DIRECT, etc.).
A simple alias would NOT have worked here, unlike process_techniques_files.py's
equivalent fix - the member names themselves differed in casing, not just
which module defined them.

Known bug, confirmed by actually running the real grid -> count ->
analysis pipeline end-to-end (see test_csv_analysis.py): the real
production pipeline (batch/entrypoints.py's other_techniques_from_times)
calls grid_engine.count_aspect_groups_txt with flag_pssr_count_moon=False
for SECONDARY_DIRECT, writing the simpler 5-field COUNT format - but
extract_data_from_file's SECONDARY_DIRECT branch expects the moon-aware
7-field format, so every real Secondary_Direct COUNT.txt file currently
parses to an empty DataFrame here. Not fixed as part of this phase - it's
a real behavior change, not a mechanical move, and which side should
change (this file's expectation, or the flag passed upstream) is a
judgment call for you.
"""
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from core.constants import aTechniqueType

def extract_data_from_file(filename, technique: aTechniqueType):
    str_tf = '?'
    flag_pssr = False
    match technique:
        case aTechniqueType.PRIMARY_DIRECT:
            str_tf = 'pd'
        case aTechniqueType.SECONDARY_DIRECT:
            str_tf = 'sc'
            flag_pssr = True
        case aTechniqueType.PSSR:
            str_tf = 'sr'
            flag_pssr = True
        case aTechniqueType.TRANSIT:
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
        if 'pssr' in filename:
            technique = aTechniqueType.PSSR
        elif 'prim' in filename:
            technique = aTechniqueType.PRIMARY_DIRECT
        elif 'sec' in filename:
            technique = aTechniqueType.SECONDARY_DIRECT
        elif 'tran' in filename:
            technique = aTechniqueType.TRANSIT

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

def create_csv_count_txt(filename_read_list, filename_write):
    """sort by count"""
    file_list = filename_read_list 
    final_df = load_and_concatenate_files(file_list)
    final_df_sorted = final_df.sort_values(by=['all-pd'], ascending=[False])
  
    final_df.to_csv(filename_write, index=False)
    #print(final_df.head())  

def main():
    file_list = ['20_10_24_2000-03-11_pssrCOUNT.txt', '20_10_24_2000-03-11_secondariesCOUNT.txt', '20_10_24_2000-03-11_transitCOUNT.txt']  
    final_df = load_and_concatenate_files(file_list)
    final_df_sorted = final_df.sort_values(by=['mon-conj-sr','mon-maj-sr'], ascending=[False, False])
  
    final_df_sorted.to_csv('20_10_ver1_sorted_planet_data.csv', index=False)
    #print(final_df.head())  

