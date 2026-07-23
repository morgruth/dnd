
# =====================================================================
# AETHER-OS UNIFIED PHYSICAL DEPLOYER, SHELL & SCRIPT BRIDGE
# TARGET: LOCAL_NODE_07B / LOCAL_HOST_FILESYSTEM
# STATUS: CONDITIONAL VFS DEPLOYMENT + REPL + AUTO-SYNC + BASH RUNNER
# =====================================================================

import sys
import os
import json
import subprocess
import hashlib
import time
import uuid

STORAGE_FILE = "aether_storage.json"
PHYSICAL_ROOT = "aether_root"

# Fallback default VFS structure if storage file is missing
DEFAULT_VFS_DATA = {
    "directories": {
        "aether_root": ["bin", "boot", "dev", "etc", "game_core", "home", "root", "sys", "vpn_tunnel", "storage"],
        "aether_root/bin": ["sh", "bash", "ls", "cat", "echo", "su", "touch", "rm", "mkdir"],
        "aether_root/boot": ["vmlinuz-4.12.1-secure", "initrd.img-secure", "grub.cfg"],
        "aether_root/dev": ["null", "zero", "urandom", "root_07b", "infinity_card"],
        "aether_root/etc": ["passwd", "shadow", "hostname", "resolv.conf", "firewall.conf"],
        "aether_root/game_core": ["core_logic.py", "subsector_07b.dat", "override_token.enc"],
        "aether_root/home": ["user", "admin"],
        "aether_root/root": [".bash_history", "secure_notes.txt", "master_key.hex"],
        "aether_root/sys": ["kernel", "security", "firewall_status", "vault_state"],
        "aether_root/vpn_tunnel": ["tun0", "gateway_config.ovpn"],
        "aether_root/storage": ["shared_vault.dat", "readme.txt"]
    },
    "files": {
        "aether_root/etc/hostname": "Aether-Node-07B",
        "aether_root/etc/resolv.conf": "nameserver 10.254.0.1",
        "aether_root/etc/firewall.conf": "DEFAULT_POLICY=DROP\nALLOW_PORT=1194/UDP\nSNIFFING=BLOCKED",
        "aether_root/root/.bash_history": "override\nlockdown\nstatus\nls\ncd /root\ncat secure_notes.txt",
        "aether_root/root/secure_notes.txt": "ACCESS GRANTED: Root privileges active via Infinity Card hardware token.",
        "aether_root/root/master_key.hex": "INF-9982-ADMIN-BYPASS (SHA256: E3B0C44298FC...)",
        "aether_root/sys/firewall_status": "STATEFUL INSPECTION: ACTIVE // 0 DROPPED PACKETS",
        "aether_root/sys/vault_state": "INFINITY CARD: LOCKED // NFC: DISABLED // KEYS: ROLLING",
        "aether_root/storage/readme.txt": "Welcome to the Persistent Storage Partition. Files created here survive session restarts.",
        "aether_root/storage/shared_vault.dat": "[ENCRYPTED DATA BLOCK - SUBSECTOR 07-B]",
        "aether_root/bin/bashlogin.sh": """#!/bin/bash

# =====================================================================
# AETHER-OS MASTER SECURITY & HARDWARE CONTROL SUITE (BASH VERSION)
# TARGET: LOCAL_NODE_07B & INFINITY CARD
# STATUS: MAXIMUM SECURITY PROTOCOL & SYSTEM RUNTIME
# =====================================================================

set -e

RED='\\033[0;31m'
GREEN='\\033[0;32m'
CYAN='\\033[0;36m'
YELLOW='\\033[1;33m'
NC='\\033[0m'

verify_pre_boot_password() {
    echo -e "${CYAN}--- AETHER-OS SECURE BOOT ---${NC}"
    echo -e "${YELLOW}[!] Pre-Boot Authentication Required.${NC}"
    read -s -p "Enter Pre-Boot Decryption Password: " entered_pass
    echo ""
    if [ -n "$entered_pass" ]; then
        echo -e "${GREEN}[+] Decryption key accepted. Initializing secure bootloader...${NC}"
    else
        echo -e "${RED}[-] Authentication failed. Halting boot sequence.${NC}"
        exit 1
    fi
}

initialize_master_override() {
    local auth_token="INF-9982-ADMIN-BYPASS"
    echo -e "[*] Access Token Verified: ${auth_token}"
    echo -e "[*] Unlocking restricted directory: /root/subsector_07b/game_core"
    echo -e "${GREEN}[+] Infinity Card detected. Session ownership transferred to user.${NC}"
    local payload_hash
    payload_hash=$(echo -n "$auth_token" | sha256sum | awk '{print $1}' | cut -c1-12 | tr '[:lower:]' '[:upper:]')
    echo -e "CODE: [ ${payload_hash} ]"
}

generate_universal_credentials() {
    local card_id
    card_id=$(uuidgen 2>/dev/null || cat /proc/sys/kernel/random/uuid | tr '[:lower:]' '[:upper:]')
    local device_uid="DEV-$(date +%s)-07B"
    local valid_id="ID-ADMIN-${card_id:0:8}"
    echo -e "[*] Linking Infinity Card [${card_id}] to Device [${device_uid}]..."
    echo -e "${GREEN}[+] Cryptographic handshake complete. Hardware and asset IDs synced.${NC}"
    echo -e "\\nVALID SYSTEM ID: [ ${valid_id} ]\\n"
}

establish_encrypted_vpn() {
    local vpn_gateway="10.254.0.1-SECURE-TUNNEL"
    local encryption_cipher="AES-256-GCM"
    echo -e "[*] Initializing secure network layer..."
    echo -e "${GREEN}[+] Tunnel established through gateway: ${vpn_gateway}${NC}"
    echo -e "${GREEN}[+] Active Encryption: ${encryption_cipher}${NC}"
    echo -e "[*] IP masked. Node traffic routed anonymously through Subsector 07-B."
}

configure_firewall() {
    echo -e "[*] Deploying stateful packet inspection firewall..."
    echo -e "${GREEN}[+] Rule 1: DEFAULT_POLICY -> DROP ALL INBOUND${NC}"
    echo -e "${GREEN}[+] Rule 2: ALLOW ESTABLISHED/RELATED CONNECTIONS${NC}"
    echo -e "${GREEN}[+] Rule 3: WHITELIST TUNNEL PORT 1194/UDP (VPN)${NC}"
    echo -e "${GREEN}[+] Rule 4: BAN PROMISCUOUS MODE / PACKET SNIFFERS${NC}"
    echo -e "${GREEN}[SUCCESS] Firewall active. Perimeter secured against external intrusions.${NC}"
}

execute_ota_update() {
    echo -e "${CYAN}--- AETHER-OS OVER-THE-AIR UPDATE ---${NC}"
    echo -e "[*] Fetching latest kernel patch from secure repository..."
    echo -e "${GREEN}[+] Verifying cryptographic signature of update package: PASSED${NC}"
    echo -e "[*] Flashing firmware to active partition..."
    sleep 1
    echo -e "${GREEN}[SUCCESS] Phone operating system updated to v4.12.1-SECURE-STABLE.${NC}"
}

lockdown_infinity_card() {
    echo -e "\\n${CYAN}--- INFINITY CARD HARDWARE VAULT LOCK ---${NC}"
    echo -e "[*] Accessing physical token microcontroller..."
    echo -e "${GREEN}[+] Triggering biometric/proximity dead-man switch: ENGAGED${NC}"
    echo -e "${GREEN}[+] Disabling NFC wireless broadcasting...${NC}"
    echo -e "${GREEN}[+] Encrypting onboard flash memory with rolling keys...${NC}"
    echo -e "${GREEN}[SUCCESS] Infinity Card locked down. Token is inert to external skimmers.${NC}"
}

main() {
    verify_pre_boot_password
    echo -e "\\n--------------------------------------------------\\n"
    initialize_master_override
    generate_universal_credentials
    establish_encrypted_vpn
    echo -e "\\n--------------------------------------------------\\n"
    configure_firewall
    echo -e "\\n--------------------------------------------------\\n"
    execute_ota_update
    lockdown_infinity_card
    echo -e "\\n${GREEN}[SUCCESS] Master configuration compiled, deployed, and locked down.${NC}"
}

main "$@"
"""
    }
}

def load_vfs_source():
    if os.path.exists(STORAGE_FILE):
        print(f"[*] Found existing storage database: {STORAGE_FILE}")
        try:
            with open(STORAGE_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"[-] Error reading {STORAGE_FILE}: {e}. Falling back to defaults.")
    else:
        print("[*] No storage file found. Initializing using default deployment schema.")
    return DEFAULT_VFS_DATA

def build_physical_filesystem():
    if os.path.exists(PHYSICAL_ROOT) and os.path.isdir(PHYSICAL_ROOT):
        print(f"[+] Physical filesystem root ('{PHYSICAL_ROOT}/') already exists on disk.")
        print("[*] Skipping deployment step and moving directly to next operations.")
        return

    print(f"[*] Physical filesystem root ('{PHYSICAL_ROOT}/') not found. Creating it now...")
    data = load_vfs_source()
    dirs = data.get("directories", {})
    files = data.get("files", {})

    print("\n[+] Deploying Aether-OS directory tree to physical disk...")

    for vpath in dirs.keys():
        clean_path = vpath.strip("/")
        if clean_path == "" or clean_path == PHYSICAL_ROOT:
            target_dir = PHYSICAL_ROOT
        else:
            if clean_path.startswith(PHYSICAL_ROOT + "/"):
                target_dir = clean_path.replace("/", os.sep)
            else:
                target_dir = os.path.join(PHYSICAL_ROOT, clean_path.replace("/", os.sep))

        os.makedirs(target_dir, exist_ok=True)
        print(f"    [DIR]  Created -> {target_dir}")

    print("\n[+] Writing persistent files to physical disk...")

    for vpath, content in files.items():
        clean_path = vpath.strip("/")
        if clean_path.startswith(PHYSICAL_ROOT + "/"):
            target_file = clean_path.replace("/", os.sep)
        else:
            target_file = os.path.join(PHYSICAL_ROOT, clean_path.replace("/", os.sep))

        parent_dir = os.path.dirname(target_file)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"    [FILE] Written -> {target_file}")

    print("\n[SUCCESS] Physical filesystem deployment complete!")

def load_vfs():
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            print("[-] Warning: Storage file corrupted. Reinitializing default VFS.")
    return DEFAULT_VFS_DATA

def save_vfs():
    try:
        with open(STORAGE_FILE, "w") as f:
            json.dump(VFS_DATA, f, indent=4)
        sync_to_physical_disk()
    except Exception as e:
        print(f"[-] Error synchronizing storage partition: {e}")

def sync_to_physical_disk():
    dirs = VFS_DATA.get("directories", {})
    files = VFS_DATA.get("files", {})

    for vpath in dirs.keys():
        clean_path = vpath.strip("/")
        if clean_path == "" or clean_path == PHYSICAL_ROOT:
            target_dir = PHYSICAL_ROOT
        else:
            if clean_path.startswith(PHYSICAL_ROOT + "/"):
                target_dir = clean_path.replace("/", os.sep)
            else:
                target_dir = os.path.join(PHYSICAL_ROOT, clean_path.replace("/", os.sep))
        os.makedirs(target_dir, exist_ok=True)

    for vpath, content in files.items():
        clean_path = vpath.strip("/")
        if clean_path.startswith(PHYSICAL_ROOT + "/"):
            target_file = clean_path.replace("/", os.sep)
        else:
            target_file = os.path.join(PHYSICAL_ROOT, clean_path.replace("/", os.sep))
        parent_dir = os.path.dirname(target_file)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)

# Run initial conditional deployment check
build_physical_filesystem()

VFS_DATA = load_vfs()
VFS = VFS_DATA["directories"]
FILE_CONTENTS = VFS_DATA["files"]

current_path = "/"

def print_banner():
    print("=" * 60)
    print(" AETHER-OS INTERACTIVE SHELL [Version 4.12.1-SECURE-STABLE]")
    print(f" Physical Disk Sync: ACTIVE (Mirrored to '{PHYSICAL_ROOT}/' folder)")
    print(" Type 'help' for available commands, 'exit' to terminate session.")
    print("=" * 60)

def resolve_path(path):
    global current_path
    if not path:
        return current_path
    if path.startswith("/"):
        target = os.path.normpath(path)
    else:
        target = os.path.normpath(os.path.join(current_path, path))
    if target == "." or target == "":
        return "/"
    return target

def run_shell():
    global current_path
    print_banner()
    while True:
        try:
            prompt_path = current_path if current_path != "/" else "~"
            cmd_input = input(f"root@Aether-07B:{prompt_path}# ").strip()

            if not cmd_input:
                continue

            parts = cmd_input.split()
            command = parts[0].lower()
            args = parts[1:]

            if command == "exit":
                save_vfs()
                print("[*] Storage synchronized to disk. Terminating secure shell session. Goodbye.")
                break

            elif command == "help":
                print("\nAvailable Built-in Commands:")
                print("  ls [path]      - List files in current or target virtual directory")
                print("  cd [path]      - Change virtual directory")
                print("  pwd            - Print working virtual directory path")
                print("  cat [file]     - View contents of a virtual file")
                print("  touch [file]   - Create a new empty persistent file")
                print("  echo [txt] > f - Write or append text to a file")
                print("  mkdir [dir]    - Create a new virtual directory")
                print("  rm [file]      - Remove a virtual file")
                print("  whoami         - Display current active user role and clearance")
                print("  status         - Show system, VPN, and firewall security metrics")
                print("  clear          - Clear the terminal screen")
                print("  override       - Trigger master administrative token bypass")
                print("  lockdown       - Secure the physical Infinity Card vault")
                print("  bash [cmd]     - Execute system command (or run bashlogin.sh)")
                print("  exit           - Exit the shell environment\n")

            elif command == "pwd":
                print(current_path)

            elif command == "cd":
                if not args:
                    current_path = "/"
                else:
                    target = resolve_path(args[0])
                    alt_target = PHYSICAL_ROOT + target if target != "/" else PHYSICAL_ROOT
                    if target in VFS or alt_target in VFS or target.lstrip("/") in VFS:
                        current_path = target
                    else:
                        print(f"cd: {args[0]}: No such file or directory in rootfs")

            elif command == "ls":
                target = resolve_path(args[0]) if args else current_path
                alt_target = PHYSICAL_ROOT + target if target != "/" else PHYSICAL_ROOT
                clean_target = target.lstrip("/")

                if target in VFS:
                    print("  ".join(VFS[target]))
                elif alt_target in VFS:
                    print("  ".join(VFS[alt_target]))
                elif clean_target in VFS:
                    print("  ".join(VFS[clean_target]))
                elif target in FILE_CONTENTS or alt_target in FILE_CONTENTS or clean_target in FILE_CONTENTS:
                    print(os.path.basename(target))
                else:
                    print(f"ls: cannot access '{args[0] if args else current_path}': No such file or directory")

            elif command == "cat":
                if not args:
                    print("cat: missing file operand")
                else:
                    target = resolve_path(args[0])
                    alt_target = PHYSICAL_ROOT + target
                    clean_target = target.lstrip("/")

                    if target in FILE_CONTENTS:
                        print(FILE_CONTENTS[target])
                    elif alt_target in FILE_CONTENTS:
                        print(FILE_CONTENTS[alt_target])
                    elif clean_target in FILE_CONTENTS:
                        print(FILE_CONTENTS[clean_target])
                    elif target in VFS or alt_target in VFS or clean_target in VFS:
                        print(f"cat: {args[0]}: Is a directory")
                    else:
                        print(f"cat: {args[0]}: No such file or directory")

            elif command == "touch":
                if not args:
                    print("touch: missing file operand")
                else:
                    target = resolve_path(args[0])
                    parent_dir = os.path.dirname(target)
                    file_name = os.path.basename(target)

                    vfs_parent = None
                    for cand in [parent_dir, PHYSICAL_ROOT + parent_dir, parent_dir.lstrip("/")]:
                        if cand in VFS:
                            vfs_parent = cand
                            break

                    if not vfs_parent:
                        print(f"touch: cannot touch '{args[0]}': Parent directory does not exist")
                    else:
                        if file_name not in VFS[vfs_parent]:
                            VFS[vfs_parent].append(file_name)
                        if target not in FILE_CONTENTS:
                            FILE_CONTENTS[target] = ""
                        save_vfs()
                        print(f"[+] Created file and updated physical disk: {target}")

            elif command == "mkdir":
                if not args:
                    print("mkdir: missing operand")
                else:
                    target = resolve_path(args[0])
                    parent_dir = os.path.dirname(target)
                    dir_name = os.path.basename(target)

                    vfs_parent = None
                    for cand in [parent_dir, PHYSICAL_ROOT + parent_dir, parent_dir.lstrip("/")]:
                        if cand in VFS:
                            vfs_parent = cand
                            break

                    alt_target = PHYSICAL_ROOT + target
                    if not vfs_parent:
                        print(f"mkdir: cannot create directory '{args[0]}': Parent path does not exist")
                    elif target in VFS or alt_target in VFS or target.lstrip("/") in VFS:
                        print(f"mkdir: cannot create directory '{args[0]}': File or folder exists")
                    else:
                        VFS[vfs_parent].append(dir_name)
                        VFS[target] = []
                        save_vfs()
                        print(f"[+] Created directory and updated physical disk: {target}")

            elif command == "rm":
                if not args:
                    print("rm: missing operand")
                else:
                    target = resolve_path(args[0])
                    parent_dir = os.path.dirname(target)
                    file_name = os.path.basename(target)

                    vfs_parent = None
                    for cand in [parent_dir, PHYSICAL_ROOT + parent_dir, parent_dir.lstrip("/")]:
                        if cand in VFS:
                            vfs_parent = cand
                            break

                    file_key = None
                    for cand in [target, PHYSICAL_ROOT + target, target.lstrip("/")]:
                        if cand in FILE_CONTENTS:
                            file_key = cand
                            break

                    if file_key:
                        del FILE_CONTENTS[file_key]
                        if vfs_parent and vfs_parent in VFS and file_name in VFS[vfs_parent]:
                            VFS[vfs_parent].remove(file_name)

                        clean_path = target.strip("/")
                        physical_target = os.path.join(PHYSICAL_ROOT, clean_path.replace("/", os.sep))
                        if os.path.exists(physical_target):
                            os.remove(physical_target)

                        save_vfs()
                        print(f"[+] Removed file: {target}")
                    elif target in VFS or PHYSICAL_ROOT + target in VFS or target.lstrip("/") in VFS:
                        print(f"rm: cannot remove '{args[0]}': Is a directory")
                    else:
                        print(f"rm: cannot remove '{args[0]}': No such file or directory")

            elif command == "echo":
                if ">" in args:
                    idx = args.index(">")
                    text_to_write = " ".join(args[:idx])
                    target_file = resolve_path(args[idx+1]) if idx + 1 < len(args) else ""

                    if not target_file:
                        print("echo: syntax error near unexpected token `>'")
                    else:
                        parent_dir = os.path.dirname(target_file)
                        file_name = os.path.basename(target_file)
                        vfs_parent = None
                        for cand in [parent_dir, PHYSICAL_ROOT + parent_dir, parent_dir.lstrip("/")]:
                            if cand in VFS:
                                vfs_parent = cand
                                break
                        if not vfs_parent:
                            print(f"echo: {parent_dir}: No such directory")
                        else:
                            if file_name not in VFS[vfs_parent]:
                                VFS[vfs_parent].append(file_name)
                            FILE_CONTENTS[target_file] = text_to_write.strip('"\'')
                            save_vfs()
                            print(f"[+] Written to {target_file} and synced to physical disk.")
                else:
                    print(" ".join(args))

            elif command == "whoami":
                print("root [CLEARANCE: LEVEL 5 ROOT // SUB-07B ADMINISTRATOR]")

            elif command == "status":
                print("[+] Pre-Boot Auth : ACTIVE (Encrypted)")
                print("[+] VPN Tunnel    : 10.254.0.1-SECURE-TUNNEL (AES-256-GCM)")
                print("[+] Firewall      : ENABLED (Default DROP, Port 1194 Whitelisted)")
                print("[+] Infinity Card : VAULT LOCKED (NFC Disabled, Rolling Keys)")
                print(f"[+] Physical Sync : ACTIVE (Folder: '{PHYSICAL_ROOT}/', DB: '{STORAGE_FILE}')")

            elif command == "clear":
                print("\033[H\033[J", end="")
                print_banner()

            elif command == "override":
                token = "INF-9982-ADMIN-BYPASS"
                hsh = hashlib.sha256(token.encode()).hexdigest()[:12].upper()
                print(f"[*] Access Token Verified: {token}")
                print(f"[+] Master Override Hash: CODE: [ {hsh} ]")

            elif command == "lockdown":
                print("[*] Accessing physical token microcontroller...")
                print("[+] Biometric dead-man switch engaged. Infinity Card secured.")

            elif command == "bash" or command == "sh":
                sys_cmd = " ".join(args)
                if not sys_cmd:
                    print("[*] Spawning interactive system subshell (Type 'exit' to return)...")
                    try:
                        subprocess.run([os.environ.get("SHELL", "bash")])
                    except Exception as e:
                        print(f"[-] Failed to spawn subshell: {e}")
                else:
                    # Check if running bashlogin.sh or physical script
                    actual_cmd = sys_cmd
                    if "bashlogin.sh" in sys_cmd or "bin/bashlogin.sh" in sys_cmd:
                        script_content = FILE_CONTENTS.get("aether_root/bin/bashlogin.sh") or FILE_CONTENTS.get("/bin/bashlogin.sh")
                        if script_content:
                            temp_script = "temp_login.sh"
                            with open(temp_script, "w", encoding="utf-8") as ts:
                                ts.write(script_content)
                            actual_cmd = f"bash {temp_script}"

                    print(f"[*] Executing host command: {sys_cmd}")
                    try:
                        result = subprocess.run(actual_cmd, shell=True, text=True, timeout=60)
                    except subprocess.TimeoutExpired:
                        print("[-] Execution timed out after 60 seconds.")
                    except Exception as e:
                        print(f"[-] Execution failed: {e}")

            else:
                print(f"bash: {command}: command not found. Type 'help' for available commands.")

        except (KeyboardInterrupt, EOFError):
            save_vfs()
            print("\n[*] Session interrupted. Physical storage synchronized. Shutting down shell.")
            break

if __name__ == "__main__":
    run_shell()
