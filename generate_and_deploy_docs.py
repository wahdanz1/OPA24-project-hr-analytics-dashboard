import shutil
from pathlib import Path
import subprocess
from config import dbt_folder

if __name__ == "__main__":
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