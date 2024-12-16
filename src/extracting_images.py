import fitz
import re
import numpy as np
from src.open_ocr import get_names,get_OCR
import pandas as pd
import os
from time import perf_counter as counter
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import pandas as pd
from typing import Tuple, List
import tempfile
import time
import openai
from src.pattern import patterns, pattern_req

# Global variables to track requests and implement throttling
REQUESTS_PER_MINUTE = 13  # Safety margin to avoid hitting the limit
REQUEST_INTERVAL = 60 / REQUESTS_PER_MINUTE  # Interval between requests in seconds
last_request_time = 0  # To track the time of the last request

def throttled_get_OCR(temp_filename: str) -> dict:
    """
    Throttled wrapper for get_OCR with retry mechanism.
    """
    global last_request_time

    # Throttle requests
    time_since_last_request = time.time() - last_request_time
    if time_since_last_request < REQUEST_INTERVAL:
        time.sleep(REQUEST_INTERVAL - time_since_last_request)

    while True:
        try:
            # Call the API
            ocr_data = get_OCR(temp_filename)
            last_request_time = time.time()  # Update the last request time
            return ocr_data
        except openai.RateLimitError as e:
            print(f"Rate limit reached: {e}. Retrying after 2 seconds...")
            time.sleep(2)  # Retry after a short delay
        except Exception as e:
            print(f"Unexpected error during OCR: {e}")
            raise  # Re-raise unexpected errors


def reconstruct_arabic_text(text):
    # Remove unnecessary characters (like extra dashes and spaces between letters)
    cleaned_text = re.sub(r'[ـ\s]+', '  ', text)  # Remove Tatweel and excessive spaces
    return cleaned_text

def extract_cat(text):
   
    pattern = patterns
    for p in pattern:
            matches = re.finditer(p, text)
            for match in matches:
                category_id = match.group(1)
                if category_id:
                    return category_id


def extract_request_number(text):
    pattern = pattern_req
    for p in pattern:
            matches = re.finditer(p, text)
            for match in matches:
                category_id = match.group(1)
                if category_id:
                    return category_id


    


def process_single_page(args: Tuple[str, int, str]) -> List[Tuple[str, str, int, str]]:
    pdf_path, page_number, output_folder = args
    results = []
    try:
        # print(f"Processing page {page_number + 1} of {pdf_path}...")
        doc = fitz.open(pdf_path)
        page = doc[page_number]
        
        # Extract text and category
        text = page.get_text()
        category = extract_cat(text)
        request_number = extract_request_number(text)
        
        # Get images
        images = page.get_images()
        # print(f"Found {len(images)} images on page {page_number + 1}.")
        
        for img_idx, img in enumerate(images):
            xref = img[0]
            img_info = doc.extract_image(xref)
            
            with tempfile.NamedTemporaryFile(suffix=f".{img_info['ext']}", delete=False) as temp_file:
                temp_filename = temp_file.name
                temp_file.write(img_info['image'])
            
            try:
                ocr_data = throttled_get_OCR(temp_filename)
                eng, ara = get_names(ocr_data)
                results.append((ara, eng, page_number + 1, category,request_number))
            except Exception as ocr_error:
                print(f"OCR failed for file {temp_filename}: {ocr_error}")
                traceback.print_exc()
                raise               
            finally:
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
        doc.close()
    except Exception as e:
        print(f"Error processing page {page_number + 1}: {e}")
        traceback.print_exc()
    return results

def extract(pdf_path: str, output_folder: str) -> pd.DataFrame:
    """
    Extract information from PDF with parallel processing
    
    Args:
        pdf_path: Path to PDF file
        output_folder: Output folder for any necessary files
    Returns:
        DataFrame containing extracted information
    """
    start = counter()
    
    # Get total pages without keeping document open
    with fitz.open(pdf_path) as doc:
        total_pages = len(doc)
    
    # Prepare arguments for parallel processing
    page_args = [
        (pdf_path, page_num, output_folder)
        for page_num in range(total_pages)
    ]
    
    # Calculate optimal number of workers
    max_workers = max(1, multiprocessing.cpu_count() - 1)
    
    # Process pages in parallel
    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        
        # Submit all jobs
        for args in page_args:
            future = executor.submit(process_single_page, args)
            futures.append(future)
        
        # Collect results as they complete
        for future in futures:
            try:
                page_results = future.result()
                results.extend(page_results)
            except Exception as e:
                print(f"Error processing page: {e}")
    
    # Create DataFrame
    if results:
        df = pd.DataFrame(results, 
                         columns=["Magazine_Arabic_Name", "Magazine_English_Name", "Magazine_Page_Number", "Magazine_Category_id","Request Number"])
    else:
        df = pd.DataFrame(columns=["Magazine_Arabic_Name", "Magazine_English_Name", "Magazine_Page_Number", "Magazine_Category_id","Request Number"])
    
    end = counter()
    # print(f"Taking {end - start} sec to process {total_pages} pages using parallel processing")
    
    return df

# Version with progress bar
def extract_with_progress(pdf_path: str, output_folder: str) -> pd.DataFrame:
    """
    Version of extract() with progress monitoring
    """
    from tqdm import tqdm
    
    # Get total pages
    with fitz.open(pdf_path) as doc:
        total_pages = len(doc)
    
    # Prepare arguments
    page_args = [
        (pdf_path, page_num, output_folder)
        for page_num in range(total_pages)
    ]
    
    results = []
    with tqdm(total=total_pages, desc="Processing PDF") as pbar:
        with ProcessPoolExecutor(max_workers=max(1, multiprocessing.cpu_count() - 1)) as executor:
            futures = []
            
            # Submit all jobs
            for args in page_args:
                future = executor.submit(process_single_page, args)
                futures.append(future)
            
            # Collect results as they complete
            for future in futures:
                try:
                    page_results = future.result()
                    results.extend(page_results)
                    pbar.update(1)
                except Exception as e:
                    print(f"Error processing page: {e}")
                    pbar.update(1)
    
    return pd.DataFrame(results, 
                       columns=["Magazine_Arabic_Name", "Magazine_English_Name", "Magazine_Page_Number", "Magazine_Category_id","Request Number"])

# Optional: Add error handling wrapper
import traceback

def safe_extract(pdf_path: str, output_folder: str, with_progress: bool = True) -> pd.DataFrame:
    """
    Wrapper function with detailed error logging
    """
    try:
        if with_progress:
            return extract_with_progress(pdf_path, output_folder)
        return extract(pdf_path, output_folder)
    except Exception as e:
        # Log detailed traceback
        print(f"Error processing PDF: {e}")
        traceback.print_exc()
        
        # Return an empty DataFrame with the correct structure
        return pd.DataFrame(columns=["Magazine_Arabic_Name", "Magazine_English_Name", "Magazine_Page_Number", "Magazine_Category_id","Request Number"])
