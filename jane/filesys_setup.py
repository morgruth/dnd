
# =====================================================================
# AETHER-OS PHYSICAL VFS DEPLOYER
# TARGET: LOCAL_HOST_FILESYSTEM (Subsector 07-B)
# STATUS: UNPACKING PERSISTENT STORAGE DIRECTORIES & FILES TO DISK
# =====================================================================

import os
import json

STORAGE_FILE = "aether_storage.json"

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
        "aether_root/storage/shared_vault.dat": "[ENCRYPTED DATA BLOCK - SUBSECTOR 07-B]"
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
    data = load_vfs_source()
    dirs = data.get("directories", {})
    files = data.get("files", {})

    print("\n[+] Deploying Aether-OS directory tree to physical disk...")

    # Create directories
    for vpath in dirs.keys():
        # Convert virtual paths (e.g., '/' or '/root') into local subfolder structure under 'aether_root'
        clean_path = vpath.strip("/")
        if clean_path == "":
            target_dir = "aether_root"
        else:
            target_dir = os.path.join("aether_root", clean_path.replace("/", os.sep))

        os.makedirs(target_dir, exist_ok=True)
        print(f"    [DIR]  Created -> {target_dir}")

    print("\n[+] Writing persistent files to physical disk...")

    # Write files
    for vpath, content in files.items():
        clean_path = vpath.strip("/")
        target_file = os.path.join("aether_root", clean_path.replace("/", os.sep))

        # Ensure parent directory exists just in case
        parent_dir = os.path.dirname(target_file)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"    [FILE] Written -> {target_file}")

    print("\n[SUCCESS] Physical filesystem deployment complete!")
    print("[*] You can now browse the real files directly inside your machine's 'aether_root' folder.")

if __name__ == "__main__":
    build_physical_filesystem()
