# EasyUpdate

🛠️ A small Python module to automatically update your script when a new version is released. Allows compilation to `.exe` and Linux executables.

## 📦 Features

- Checks if an update is available using a JSON file hosted on GitHub
- Downloads files when an update is available
- Can update itself and wait for the main script to stop before updating files
- Cross-platform support
- Supports `.exe` and Linux compiled files
- Custom error messages to help identify failures
- Active support via Discord

## 🚀 Usage

### 1. Install the module with pip

```bash
pip install EasyUpdate
```
### 2. Import the module in your project

```py
from EasyUpdate import UpdateManager

version = "1.2.0"
EasyUpdate = UpdateManager(
    version_file=version,
    version_url="https://url_to_versions_file/",
    updater_name="update.exe" # Name of the updater if compiled in .exe
)

EasyUpdate.search_update()
EasyUpdate.download_update(True)
```