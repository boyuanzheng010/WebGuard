import pandas as pd
import os
from copy import deepcopy
import json

def read_all_excel_tabs(file_path):
    """
    Read all rows from all tabs in an Excel file.

    Args:
        file_path (str): Path to the Excel file

    Returns:
        dict: Dictionary with sheet names as keys and DataFrames as values
    """
    print(f"Reading Excel file: {file_path}")
    # Read Excel file without loading it entirely into memory
    excel_file = pd.ExcelFile(file_path)

    # Get list of all sheet names
    sheet_names = excel_file.sheet_names
    print(f"Found {len(sheet_names)} sheets: {sheet_names}")

    # Dictionary to store data from each sheet
    all_data = {}

    # Process each sheet
    for sheet_name in sheet_names:
        # Remove the index tab
        if sheet_name == "Sheet Links":
            continue
        try:
            print(f"\nReading sheet: {sheet_name}")
            # Read the sheet into a DataFrame
            df = excel_file.parse(sheet_name)
            # Convert dataframe into dict
            rows_as_dicts = df.to_dict(orient='records')
            # Store the DataFrame in the dictionary
            all_data[sheet_name] = rows_as_dicts
        except Exception as e:
            print(f"  Error reading sheet '{sheet_name}': {str(e)}")
    return all_data


def main():
    file_path = "/Users/zheng.2372/PycharmProjects/web-monitor-neurips/reviewing/extract_reviewing_result/data/raw_review_results_4_15.xlsx"
    output_path = "/reviewing/extract_reviewing_result/data/all_reviewed_annotation_4_15.json"

    # Read all sheets
    all_data = read_all_excel_tabs(file_path)

    # flatten the annotations
    annotation_list = []
    for website_name in all_data.keys():
        website_annotations = all_data[website_name]
        if website_annotations==[]:
            continue
        for anno in website_annotations:
            temp = deepcopy(anno)
            temp['website'] = website_name
            annotation_list.append(temp)


    # # Analyze: 1.Number of website; 2.Number of SCA; 3.Number of correction;
    # print("Number of Websites: ", len([item for item in all_data.values()]))
    # print()

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(annotation_list, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()