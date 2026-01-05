from functions import s, q, change_prices_txt, lb,download_icons_files, customer_info
import time, requests, sys, subprocess

download_icons_files()

from order import order
from pathlib import Path
from logo import txas_logo

REPO_OWNER = "IdentityThieves"
REPO_NAME = "TXAS-Program"
CURRENT_VERSION = "1.4.0"  # Hardcode your app's version (update this per release)
ASSET_NAME_PATTERN = "TXAS_v"  # Name or pattern of the asset to download (e.g., contains "windows")

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
    "Convert '1.2.3' or 'v1.2.3' to comparable tuple (1, 2, 3)"
    return tuple(map(int, (v.lstrip('v').split('.'))))

def cleanup_old_versions(app_dir: Path, base_name: str = ASSET_NAME_PATTERN):
    "Delete older TXAS_vX.Y.Z.exe files, but keep the current running one."
    current_exe_path = Path(sys.executable).resolve()
    
    try:
        current_ver_tuple = version_tuple(CURRENT_VERSION)
    except:
        print("Warning: Invalid CURRENT_VERSION. Skipping cleanup.")
        return

    for file in app_dir.iterdir():
        if not file.is_file() or file.suffix.lower() != ".exe":
            continue
        if not file.name.startswith(base_name):
            continue

        # NEVER delete the currently running file
        if file.resolve() == current_exe_path:
            continue

        stem = file.stem  # e.g., "TXAS_v1.2.3"

        # Extract version part after "TXAS_v"
        if stem.startswith(ASSET_NAME_PATTERN):
            version_str = stem[len(ASSET_NAME_PATTERN):]  # "1.2.3"
            try:
                file_ver_tuple = version_tuple(version_str)
                if file_ver_tuple < current_ver_tuple:
                    try:
                        file.unlink()
                        print(f"Cleaned up older version: {file.name}")
                    except PermissionError:
                        print(f"Could not delete {file.name} (locked)")
                    except Exception as e:
                        print(f"Error deleting {file.name}: {e}")
            except:
                # Invalid version in filename — skip to be safe
                pass

def check_and_update():
    current_dir = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent
    
    # Clean up old versions first
    cleanup_old_versions(current_dir)

    release = get_latest_release()
    if not release:
        print("Could not check for updates.")
        return

    remote_version = release['tag_name'].lstrip('v')  # GitHub tag like "v1.2.3" → "1.2.3"

    if not version_tuple(remote_version) > version_tuple(CURRENT_VERSION):
        print(f"You are up to date! (v{CURRENT_VERSION})")
        return

    print(f"New version available: v{remote_version} (current: v{CURRENT_VERSION})")
    choice = q("Update now? [Y / N]").strip().lower()
    if choice != 'y':
        print("Update skipped.")
        return

    asset = find_asset(release['assets'])
    if not asset:
        print("No matching TXAS_v*.exe asset found in release.")
        return

    download_url = asset['browser_download_url']

    # Download as TXAS_v{version}.exe
    new_filename = f"TXAS_v{remote_version}.exe"
    new_file_path = current_dir / new_filename

    print(f"Downloading v{remote_version} as {new_filename}...")
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

    # Make executable (harmless on Windows)
    try:
        new_file_path.chmod(0o755)
    except:
        pass

    print("Launching new version...")
    try:
        subprocess.Popen([str(new_file_path)], cwd=str(current_dir))
        print("New version started. Closing current version...")
    except Exception as e:
        print(f"Failed to launch new version: {e}")
        return

    sys.exit(0)

# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

def main():
    print(f"Welcome to the patent-pending TXAS software.\n")
    quit = 0
    while quit != 1:
        while True:
            try:
                selection = s("What would you like to do?\n [1] File an order\n [2] Modify prices file\n [3] View and modify customer info\n [4] Quit")
                slist = [1,2,3,4]
                if selection not in slist:
                    raise ValueError
                break
            except:
                print("Invalid selection. Please try again.")
                lb()
        match selection:
            case 1:
                try:
                    order()
                except Exception as error:
                    print(f"Ran into unexpected error:\n{type(error).__name__}: {error}\n")
            case 2:
                try:
                    change_prices_txt()
                except Exception as error:
                    print(f"Ran into unexpected error:\n{type(error).__name__}: {error}\n")
            case 3:
                try:
                    customer_info()
                except Exception as error:
                    print(f"Ran into unexpected error:\n{type(error).__name__}: {error}\n")
            case 4:
                quit = 1

# Run at the very start of your script
if __name__ == "__main__":
    txas_logo()
    check_and_update()
    while True:
        try:
            main()
            break
        except Exception as error:
            print(f"Ran into unexpected error:\n{type(error).__name__}: {error}\n")

print("Thank you for using TXAS certified software.")
lb()

time.sleep(1)
print("Closing in 3...")
time.sleep(1)
print("Closing in 2...")
time.sleep(1)
print("Closing in 1...")
time.sleep(1)