import subprocess

def clear_database():
    try:
        # Stop the dps service
        subprocess.check_call(['sc', 'stop', 'dps'])
        
        # Navigate to the sru directory and backup the database
        subprocess.check_call(['cd', '/d', 'C:\\Windows\\System32\\sru\\'], shell=True)
        subprocess.check_call(['mv', 'SRUDB.dat', 'srudb.dat.bak'], shell=True)
        
        # Start the dps service
        subprocess.check_call(['sc', 'start', 'dps'])
        
        print("Database cleared successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to clear the database:", e)
