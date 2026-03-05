import shutil
from pathlib import Path
import argparse

# ==================== CONFIGURAÇÃO ====================
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".md", ".odt", ".xlsx", ".xls", ".pptx", ".csv"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
    "Audio": [".mp3", ".wav", ".flac", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c"],
    "Executables": [".exe", ".msi", ".app", ".dmg"],
    "Others": []
}

def get_category(ext: str) -> str:
    ext = ext.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"

def organize_files(target_dir: str, dry_run: bool = False):
    target_path = Path(target_dir).resolve()
    
    # ==================== DEBUG ====================
    print(f"🔍 DEBUG: Folder that the script is trying to use. → {target_path}")
    print(f"🔍 DEBUG: Dry-run activated? → {dry_run}")
    print(f"🔍 DEBUG: Folder exists? → {target_path.exists()}")
    
    if not target_path.exists() or not target_path.is_dir():
        print(f"❌ ERROR: Folder '{target_dir}' does not exist or is not a folder!")
        print("💡 Tip: Use double quotes if the path contains spaces.")
        return

    print(f"\n🚀 Starting to organize the folder: {target_path}")
    print("Mode: SIMULATION (dry-run)" if dry_run else "Mode: REAL (Files will be moved!)")

    moved = 0
    for item in target_path.iterdir():
        if item.is_file():
            category = get_category(item.suffix)
            dest_folder = target_path / category
            dest_folder.mkdir(exist_ok=True)

            dest_path = dest_folder / item.name
            counter = 1
            while dest_path.exists():
                dest_path = dest_folder / f"{item.stem}_{counter}{item.suffix}"
                counter += 1

            if dry_run:
                print(f"   [DRY] {item.name} → {category}/")
            else:
                shutil.move(str(item), str(dest_path))
                print(f"   ✅ Moved: {item.name} → {category}/")
            moved += 1

    print(f"\n✅ DONE! Moved Files: {moved}")

# ==================== EXECUÇÃO ====================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File Organizer Bot")
    parser.add_argument("directory", nargs="?", default=".", help="Folder for organizing (use quotation marks if there are spaces)")
    parser.add_argument("--dry-run", action="store_true", help="It simules without actually move")
    
    args = parser.parse_args()
    organize_files(args.directory, args.dry_run)