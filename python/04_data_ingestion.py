# Bronze Layer Data Ingestion

import shutil
from pathlib import Path

# Get project folder
project_path = Path(__file__).resolve().parent.parent

# Define folder paths
raw_path = project_path / "data" / "raw"
bronze_path = project_path / "data" / "bronze"

# Create Bronze folder if not available
bronze_path.mkdir(parents=True, exist_ok=True)

# Get all files from Raw folder
files = list(raw_path.iterdir())

# Copy files from Raw to Bronze
for file in files:

    if file.is_file():

        destination = bronze_path / file.name

        shutil.copy2(file, destination)

        print("Copied:", file.name)

print("\nBronze ingestion completed!")


#  Verify Bronze Layer

print("\n========== BRONZE LAYER VERIFICATION ==========")

# Get all files from Raw folder
raw_files = {
    file.name for file in raw_path.iterdir()
    if file.is_file()
}

# Get all files from Bronze folder
bronze_files = {
    file.name for file in bronze_path.iterdir()
    if file.is_file()
}

# Display file counts
print("\nTotal files in Raw:", len(raw_files))

print("Total files in Bronze:", len(bronze_files))

# Find missing files
missing_files = raw_files - bronze_files

# Find extra files
extra_files = bronze_files - raw_files

print("\nMissing Files:", missing_files)

print("Extra Files:", extra_files)

# Final verification
if raw_files == bronze_files:

    print("\nSUCCESS: All Raw files are available in Bronze!")

else:

    print("\nWARNING: Raw and Bronze files do not match.")



# =====================================================================
# REUSABLE INGESTION FRAMEWORK


def ingest_dataset(source_path, destination_path):

    try:

        # Load dataset

        df = load_dataset(source_path)


        # Display dataset information

        print("\nDataset:", source_path.name)

        print("Rows:", df.shape[0])

        print("Columns:", df.shape[1])


        # Save dataset into Bronze layer

        destination_path.parent.mkdir(
            parents=True,
            exist_ok=True)

        df.to_csv(destination_path, index=False)


        print("Ingestion Successful:", destination_path.name)

        return True


    except Exception as error:

        print("Ingestion Failed:", source_path.name)

        print("Error:", error)

        return False
