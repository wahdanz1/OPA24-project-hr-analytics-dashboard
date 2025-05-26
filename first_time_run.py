import shutil
from pathlib import Path
import subprocess
from pipeline.pipeline import run_pipeline
from config import table_name, dbt_folder

if __name__ == "__main__":
    # Run the pipeline
    is_first_time = True  # Set to True for the first run, False for subsequent runs
    run_pipeline(table_name, is_first_time)
    print("✅ Pipeline has been executed successfully.")

    # Generate dbt docs
    print("📘 Generating dbt docs...")
    subprocess.run(["dbt", "docs", "generate"], cwd=dbt_folder, check=True)

    # Define paths
    target_dir = Path(dbt_folder) / "target"
    docs_dir = Path("docs")

    # Remove old docs/ folder if exists
    if docs_dir.exists():
        shutil.rmtree(docs_dir)
    
    # Copy fresh docs from target/ to docs/
    shutil.copytree(target_dir, docs_dir)
    print("✅ dbt documentation copied to /docs/ and ready for GitHub Pages.")