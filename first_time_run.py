from pipeline.pipeline import run_pipeline
from config import table_name


if __name__ == "__main__":
    # Run the pipeline
    is_first_time = True  # Set to True for the first run, False for subsequent runs
    run_pipeline(table_name, is_first_time)
    print("Pipeline has been executed successfully.")