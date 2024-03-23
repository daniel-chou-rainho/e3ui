import subprocess
import os

def get_csv():
    try:
        # Construct the path to the Downloads folder dynamically
        downloads_dir = os.path.join(os.environ['USERPROFILE'], 'Downloads')
        csv_file_path = os.path.join(downloads_dir, 'srumutil.csv')  # Assuming the output file is named 'srumutil.csv'
        
        # Ensure any existing instance of the file is removed to avoid confusion
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)
        
        # Run the command
        subprocess.check_call(['powercfg.exe', '/srumutil'], cwd=downloads_dir)
        
        # Check if the file was created
        if os.path.exists(csv_file_path):
            print(f"CSV file generated successfully at {csv_file_path}.")
            return csv_file_path  # Return the path to the generated CSV file
        else:
            print("Failed to generate CSV file: File does not exist.")
            return None
    except subprocess.CalledProcessError as e:
        print("Failed to generate CSV file:", e)
        return None
