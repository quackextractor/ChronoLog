import shutil
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"


def clear_directory(path: Path):
    if not path.exists():
        print(f"Directory '{path}' does not exist.")
        return

    try:
        shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)
        print(f"Successfully cleared '{path}'")
    except Exception as e:
        print(f"Failed to clear '{path}': {e}")


def user_prompt():
    options = {
        '1': lambda: clear_directory(INPUT_DIR),
        'input': lambda: clear_directory(INPUT_DIR),
        '2': lambda: clear_directory(OUTPUT_DIR),
        'output': lambda: clear_directory(OUTPUT_DIR),
        '3': lambda: (clear_directory(INPUT_DIR), clear_directory(OUTPUT_DIR)),
        'both': lambda: (clear_directory(INPUT_DIR), clear_directory(OUTPUT_DIR)),
        '0': lambda: print("Exiting without making changes.")
    }

    while True:
        choice = input("What do you want to clear? (0:exit/1:input/2:output/3:both):\n").strip().lower()
        action = options.get(choice)
        if action:
            action()
            break
        else:
            print("Invalid option. Please enter 0, 1, 2, or 3.")


if __name__ == "__main__":
    user_prompt()