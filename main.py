from functions import s, q, change_prices_txt, lb,download_icons_files

download_icons_files()

from order import order
import time, requests, sys, subprocess
from pathlib import Path

REPO_OWNER = "IdentityThieves"
REPO_NAME = "TXAS-Program"
CURRENT_VERSION = "1.2.0"  # Hardcode your app's version (update this per release)
ASSET_NAME_PATTERN = "TXAS.exe"  # Name or pattern of the asset to download (e.g., contains "windows")

def main():
    print(f"Welcome to the patent-pending TXAS software.")
    quit = 0
    while quit != 1:
        while True:
            try:
                selection = s("What would you like to do?\n [1] File an order\n [2] Modify prices file\n [3] Quit")
                slist = [1,2,3]
                if selection not in slist:
                    raise ValueError
                break
            except:
                print("Invalid selection. Please try again.")
                lb()
        match selection:
            case 1:
                #try:
                order()
                #except:
                    #print("Ran into unexpected error.\n")
            case 2:
                try:
                    change_prices_txt()
                except:
                    print("Ran into unexpected error.\n")
            case 3:
                quit = 1

def get_latest_release():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
    try:
        response = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"})
        response.raise_for_status()
        return response.json()
    except:
        return None

def version_higher(remote: str, local: str) -> bool:
    return remote.lstrip('v') > local.lstrip('v')

def find_asset(assets):
    for asset in assets:
        if ASSET_NAME_PATTERN in asset['name']:
            return asset
    return None

def version_tuple(v: str):
    """Convert version string like '1.2.3' to tuple (1, 2, 3) for comparison"""
    return tuple(map(int, (v.lstrip('v').split('.'))))

def cleanup_old_versions(app_dir: Path, base_name: str = "TXAS"):
    """Delete older version files without needing 'packaging' library."""
    current_exe_path = Path(sys.executable).resolve()
    
    # Parse current version into tuple
    try:
        current_ver_tuple = version_tuple(CURRENT_VERSION)
    except:
        print("Warning: Invalid CURRENT_VERSION format. Skipping cleanup.")
        return

    for file in app_dir.iterdir():
        if not file.is_file() or file.suffix.lower() != ".exe":
            continue
        if not file.name.startswith(base_name):
            continue

        # Never delete the running executable
        if file.resolve() == current_exe_path:
            continue

        stem = file.stem

        # Delete any _old backups
        if stem.endswith("_old"):
            try:
                file.unlink()
                print(f"Cleaned up backup: {file.name}")
            except PermissionError:
                print(f"Could not delete {file.name} (locked)")
            except Exception as e:
                print(f"Error deleting {file.name}: {e}")
            continue

        # Handle versioned files: TXAS_1.2.3.exe
        if stem.startswith(base_name + "_"):
            version_str = stem[len(base_name + "_"):]
            try:
                file_ver_tuple = version_tuple(version_str)
                if file_ver_tuple < current_ver_tuple:
                    file.unlink()
                    print(f"Cleaned up older version: {file.name} (v{version_str})")
            except:
                # Invalid version format — skip to be safe
                pass

def check_and_update():
    # First: Clean up any leftover old versions
    current_dir = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent
    cleanup_old_versions(current_dir)

    # Check for latest release
    release = get_latest_release()
    if not release:
        print("Could not check for updates.")
        return

    remote_version = release['tag_name']  # e.g., "v1.2.3" or "1.2.3"
    clean_remote = remote_version.lstrip('v')

    if not version_higher(remote_version, CURRENT_VERSION):
        print(f"You are up to date! (v{CURRENT_VERSION})\n")
        return

    print(f"New version available: {remote_version} (current: v{CURRENT_VERSION})")
    choice = input("Update now? (Y/N): ").strip().lower()
    if choice != 'y':
        print("Update skipped.\n")
        return

    asset = find_asset(release['assets'])
    if not asset:
        print("No matching executable found in release.")
        return

    download_url = asset['browser_download_url']

    # Download as TXAS_{version}.exe  (e.g., TXAS_1.2.3.exe)
    new_filename = f"TXAS_{clean_remote}.exe"
    new_file_path = current_dir / new_filename

    print(f"Downloading {remote_version} as {new_filename}...")
    try:
        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()
            with open(new_file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print("Download complete.")
    except Exception as e:
        print(f"Download failed: {e}")
        return

    # Make sure it's executable (harmless on Windows)
    try:
        new_file_path.chmod(0o755)
    except:
        pass

    print("Launching new version...")
    try:
        subprocess.Popen([str(new_file_path)], cwd=str(current_dir))
        print("New version started. Closing current version...")
    except Exception as e:
        print(f"Failed to start new version: {e}")
        return

    sys.exit(0)

# Run at the very start of your script
if __name__ == "__main__":
    check_and_update()
    #while True:
        #try:
    main()
            #break
        #except:
            #print("Ran into unexpected error. Restarting...\n")

print("Thank you for using TXAS certified software.")
lb()

time.sleep(1)
print("Closing in 3...")
time.sleep(1)
print("Closing in 2...")
time.sleep(1)
print("Closing in 1...")
time.sleep(1)