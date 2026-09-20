from pathlib import Path
import shutil
import logging

# File categories
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".webm"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".java", ".cpp", ".c", ".js", ".html", ".css", ".sql"]
}

# Create log file
logging.basicConfig(
    filename="organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_category(extension):
    """Find the category of a file based on its extension."""

    extension = extension.lower()

    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"


def get_unique_destination(destination):
    """Prevent overwriting files with the same name."""

    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_destination = destination.with_name(
            f"{destination.stem}_{counter}{destination.suffix}"
        )

        if not new_destination.exists():
            return new_destination

        counter += 1


def organize_folder(folder_path):

    folder = Path(folder_path).expanduser().resolve()

    # Check whether folder exists
    if not folder.exists():
        print("\n❌ Folder does not exist.")
        return

    # Check whether path is a folder
    if not folder.is_dir():
        print("\n❌ The path you entered is not a folder.")
        return

    moved_files = 0

    # Read all items in the folder
    for item in folder.iterdir():

        # Ignore folders
        if not item.is_file():
            continue

        # Ignore the log file
        if item.name == "organizer.log":
            continue

        # Find category
        category = get_category(item.suffix)

        # Create category folder
        category_folder = folder / category
        category_folder.mkdir(exist_ok=True)

        # Destination path
        destination = category_folder / item.name

        # Prevent duplicate filenames
        destination = get_unique_destination(destination)

        try:

            # Move the file
            shutil.move(str(item), str(destination))

            print(f"✅ {item.name}  →  {category}/")

            logging.info(
                f"Moved {item.name} to {category}"
            )

            moved_files += 1

        except Exception as error:

            print(f"❌ Error moving {item.name}: {error}")

            logging.error(
                f"Error moving {item.name}: {error}"
            )

    print("\n================================")
    print("     ORGANIZATION COMPLETE")
    print("================================")

    print(f"Total files organized: {moved_files}")
    print("Activity log: organizer.log")


# Main program
if __name__ == "__main__":

    print("================================")
    print("     SMART FILE ORGANIZER")
    print("================================")

    folder_path = input(
        "\nEnter the folder path to organize: "
    )

    organize_folder(folder_path)