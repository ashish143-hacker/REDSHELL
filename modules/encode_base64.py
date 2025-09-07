import os
import base64

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_ps_base64_from_file(ps_file, filename=None):
    """
    Encode an existing PowerShell .ps1 payload to Base64 and save as .ps1
    Always requires user or caller to provide a filename.
    """
    if not os.path.isfile(ps_file):
        raise FileNotFoundError(f"[!] File not found: {ps_file}")

    # If filename not provided, ask the user
    if not filename:
        while True:
            user_input = input("Enter filename for Base64 payload (without extension): ").strip()
            if user_input:
                filename = f"{user_input}.ps1"
                break
            print("[!] Filename cannot be blank. Please enter a valid name.")
    else:
        if not filename.lower().endswith(".ps1"):
            filename += ".ps1"

    file_path = os.path.join(OUTPUT_DIR, filename)

    # Read original PowerShell script
    with open(ps_file, "r", encoding="utf-8") as f:
        ps_content = f.read()

    # Base64 encode using UTF-16LE (required by PowerShell -EncodedCommand)
    b64_bytes = base64.b64encode(ps_content.encode("utf-16le"))
    b64_str = b64_bytes.decode("ascii")

    # Save Base64 string as .ps1 file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(b64_str)

    print(f"[+] Base64 PowerShell payload saved as: {file_path}")
    return file_path

# Compatibility wrapper for main.py
def generate_ps_base64(ps_file, filename=None):
    return generate_ps_base64_from_file(ps_file, filename)
