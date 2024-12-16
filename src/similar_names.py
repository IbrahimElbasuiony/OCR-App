from fuzzywuzzy import fuzz
import pandas as pd

def find_similar_names(excel, ocr_df, threshold=100, sim_cat=False):
    # Convert `name` column in excel to a list
    names_list = excel['name'].tolist()
    cat_list = excel['grp_code'].tolist()
    serial_list = excel['serial'].tolist()
    file = excel['file_no'].tolist()
    
    # Initialize a dictionary to store the results
    similar_names_dict = {}

    # Iterate through each row in ocr_df
    for _, row in ocr_df.iterrows():
        arabic_name = str(row['Magazine_Arabic_Name'])
        english_name = str(row['Magazine_English_Name'])
        if arabic_name and english_name is None:
            print(arabic_name,english_name)
        cat = row['Magazine_Category_id']
        
        # Find similar names for Arabic and English names
        similar_arabic = [
            name for name, cat_code in zip(names_list, cat_list) 
            if fuzz.token_sort_ratio(name, arabic_name) >= threshold and 
            (not sim_cat or cat_code == cat) and name != '.'
        ]
        
        similar_english = [
            name for name, cat_code in zip(names_list, cat_list) 
            if fuzz.token_sort_ratio(name, english_name) >= threshold and 
            (not sim_cat or cat_code == cat) and name != '.'
        ]

        
        # Add to dictionary
        if arabic_name not in similar_names_dict:
            similar_names_dict[arabic_name] = similar_arabic
        if english_name not in similar_names_dict:
            similar_names_dict[english_name] = similar_english
    
    # Create a list to store expanded rows
    expanded_rows = []
    
    # Iterate through original DataFrame to expand rows
    for _, row in ocr_df.iterrows():
        arabic_name = row['Magazine_Arabic_Name']
        english_name = row['Magazine_English_Name']
        cat_id = row['Magazine_Category_id']
        
        # Get similar names for the row
        similar_names = (
            similar_names_dict.get(arabic_name, []) or 
            similar_names_dict.get(english_name, [])
        )
        
        # If no similar names, add the original row
        if not similar_names:
            pass
        else:
            # Find corresponding category codes and indices for similar names
           for similar_name in similar_names:
            # Find all indices for this similar name
            similar_name_indices = [i for i, name in enumerate(names_list) if name == similar_name]
            
            # Create a row for each index
            for similar_name_index in similar_name_indices:
                similar_cat_id = cat_list[similar_name_index]
                serial = serial_list[similar_name_index]
                
                # Create a new row with the similar name
                new_row = row.copy()
                new_row['Similar_Names'] = similar_name
                new_row['Similar_Cat_Id'] = similar_cat_id
                new_row['Similar_Index'] = similar_name_index +2
                new_row['Similer_serial'] = serial
                new_row['Similar_file_no'] = file[similar_name_index]
                expanded_rows.append(new_row)
            
    # Create a new DataFrame from the expanded rows
    expanded_df = pd.DataFrame(expanded_rows).drop_duplicates()
    
    
    return expanded_df