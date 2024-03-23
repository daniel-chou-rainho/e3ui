import subprocess
import os

def get_csv():
    try:
        # Construct the path to the Downloads folder dynamically
        downloads_dir = os.path.join(os.environ['USERPROFILE'], 'Downloads')
        
        # Run the command and direct output to the Downloads folder
        subprocess.check_call(['powercfg.exe', '/srumutil'], cwd=downloads_dir)
        
        print(f"CSV file generated successfully in {downloads_dir}.")
    except subprocess.CalledProcessError as e:
        print("Failed to generate CSV file:", e)
