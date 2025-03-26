import psutil
import subprocess
import os
import time

def open_chrome():
    """
    Opens Google Chrome browser.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        subprocess.Popen('start chrome', shell=True)
        return True
    except Exception as e:
        print(f"Error opening Chrome: {str(e)}")
        return False

def open_calculator():
    """
    Opens Windows Calculator application.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        subprocess.Popen('calc', shell=True)
        return True
    except Exception as e:
        print(f"Error opening Calculator: {str(e)}")
        return False

def open_notepad():
    """
    Opens Windows Notepad application.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        subprocess.Popen('notepad', shell=True)
        return True
    except Exception as e:
        print(f"Error opening Notepad: {str(e)}")
        return False

def get_cpu_usage():
    """
    Retrieves current CPU usage percentage.
    
    Returns:
        float: CPU usage percentage
    """
    try:
        return psutil.cpu_percent(interval=1)
    except Exception as e:
        print(f"Error getting CPU usage: {str(e)}")
        return None

def get_ram_usage():
    """
    Retrieves current RAM usage statistics.
    
    Returns:
        dict: Dictionary containing total, used, and percentage of RAM usage
    """
    try:
        memory = psutil.virtual_memory()
        return {
            'total': round(memory.total / (1024 ** 3), 2),  # Convert to GB
            'used': round(memory.used / (1024 ** 3), 2),    # Convert to GB
            'percent': memory.percent
        }
    except Exception as e:
        print(f"Error getting RAM usage: {str(e)}")
        return None

def execute_shell_command(command):
    """
    Executes a shell command and returns its output.
    
    Args:
        command (str): The shell command to execute
        
    Returns:
        tuple: (stdout, stderr) from the command execution
    """
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        return stdout, stderr
    except Exception as e:
        print(f"Error executing command: {str(e)}")
        return None, str(e)

if __name__ == "__main__":
    # Example usage
    print("Opening applications...")
    open_chrome()
    time.sleep(1)
    open_calculator()
    time.sleep(1)
    open_notepad()
    
    print("\nSystem Metrics:")
    print(f"CPU Usage: {get_cpu_usage()}%")
    ram_info = get_ram_usage()
    print(f"RAM Usage: {ram_info['used']}GB / {ram_info['total']}GB ({ram_info['percent']}%)")
    
    print("\nExecuting a test shell command (dir)...")
    stdout, stderr = execute_shell_command('dir')
    print(f"Output:\n{stdout}")
    if stderr:
        print(f"Errors:\n{stderr}")