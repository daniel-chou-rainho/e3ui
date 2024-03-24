import subprocess
import time

def wait_for_service_to_stop(service_name, timeout=30):
    """
    Waits for a Windows service to stop with a given timeout.

    Args:
    - service_name: The name of the service to wait for.
    - timeout: Maximum time to wait in seconds.
    """
    start_time = time.time()
    while True:
        # Check the current status of the service using PowerShell
        result = subprocess.run(['powershell', '-Command', f"Get-Service {service_name} | Select-Object -ExpandProperty Status"], capture_output=True, text=True)
        status = result.stdout.strip()
        
        if status != "StopPending" and status != "Running":
            print(f"Service {service_name} is now in the state: {status}")
            break
        
        if time.time() - start_time > timeout:
            print(f"Timed out waiting for {service_name} service to stop.")
            break
        
        print(f"Service {service_name} is still stopping... waiting...")
        time.sleep(2)  # Wait for 2 seconds before checking again

def clear_database():
    try:
        # Attempt to stop the dps service
        subprocess.check_call(['powershell', '-Command', 'Stop-Service -Name dps -Force'])

        # Wait for the DPS service to fully stop
        wait_for_service_to_stop('dps')

        # Attempt to move the SRUDB.dat file
        move_result = subprocess.run('move C:\\Windows\\System32\\sru\\SRUDB.dat C:\\Windows\\System32\\sru\\SRUDB.dat.bak', shell=True, check=False)

        if move_result.returncode != 0:
            print("Failed to move the SRUDB.dat file. It might be in use.")
        else:
            print("SRUDB.dat file moved successfully.")

        # Attempt to start the dps service again
        subprocess.check_call(['powershell', '-Command', 'Start-Service -Name dps'])

    except subprocess.CalledProcessError as e:
        print(f"Failed to clear the database or restart the DPS service: {e}")
