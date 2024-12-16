from src.extracting_images import safe_extract
from src.similar_names import find_similar_names
import pandas as pd
from time import perf_counter as counter


def flow(pdf_path,excel_path,output_path,sim_cat=False,threshold=100):
    df = safe_extract(pdf_path=pdf_path,
             output_folder=output_path)
    df2 = pd.read_excel(excel_path)

    similer_names = find_similar_names(excel=df2,ocr_df=df,sim_cat=sim_cat,threshold=threshold)

    similer_names.to_excel(f"{output_path}/similer.xlsx")
