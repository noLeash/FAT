import os
import zipfile
import datetime

def zip_project(source_dir, output_filename):
    exclusions = {".env", "__pycache__", ".venv", ".git", ".DS_Store", ".idea", ".vscode", "node_modules"}
    extensions_to_exclude = {".pyc", ".pyo", ".log"}

    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Exclude directories
            dirs[:] = [d for d in dirs if d not in exclusions]
            
            for file in files:
                # Exclude specific extensions
                if any(file.endswith(ext) for ext in extensions_to_exclude):
                    continue
                
                file_path = os.path.join(root, file)
                archive_name = os.path.relpath(file_path, source_dir)
                
                zipf.write(file_path, archive_name)

    print(f"Project zipped successfully: {output_filename}")

if __name__ == "__main__":
    project_root = os.path.abspath(".")  # Change this if needed
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"project_backup_{timestamp}.zip"

    zip_project(project_root, zip_filename)

