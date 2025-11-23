import os
import shutil


def clear_output_directory():
    output_dir = "../output"

    if not os.path.exists(output_dir):
        print(f"Output directory '{output_dir}' does not exist.")
        return

    # Remove and recreate the directory
    shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    print(f"Successfully cleared '{output_dir}'")


if __name__ == "__main__":
    clear_output_directory()