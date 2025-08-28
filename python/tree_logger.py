import os
import sys

def print_directory_tree(start_path, indent="", is_last=False, log_file=None, current_depth=0, max_depth=None):
    """
    Recursively prints the directory tree structure relative to the start path, logging to a file.

    Args:
        start_path (str): The path to the directory to start traversing from.
        indent (str): The current indentation level for printing the tree.
        is_last (bool): Indicates if the current item is the last item in its parent directory.
        log_file (file object): The file to log the output to.
        current_depth (int): Current depth in the directory hierarchy.
        max_depth (int): Maximum depth to traverse. None means no limit.
    """
    # Check if we've reached the maximum depth
    if max_depth is not None and current_depth >= max_depth:
        return

    try:
        # Get all items in the directory
        all_items = os.listdir(start_path)
        
        # Filter out .git and target folders
        items = [item for item in all_items if not ((item == ".git" or item == "target") 
                                                   and os.path.isdir(os.path.join(start_path, item)))]
        
        num_items = len(items)

        for i, item in enumerate(items):
            item_path = os.path.join(start_path, item)
            is_last_item = (i == num_items - 1)

            if os.path.isdir(item_path):
                line = indent + ("└── " if is_last_item else "├── ") + item + "/"  # Indicate directory with "/"
                print_and_log(line, log_file)
                new_indent = indent + ("    " if is_last_item else "│   ")
                print_directory_tree(item_path, new_indent, is_last_item, log_file, current_depth + 1, max_depth)
            else:
                line = indent + ("└── " if is_last_item else "├── ") + item  # Print file names
                print_and_log(line, log_file)

    except OSError as e:
        line = f"Error accessing {start_path}: {e}"
        print_and_log(line, log_file)
    except Exception as e:
        line = f"An unexpected error occurred: {e}"
        print_and_log(line, log_file)

def print_and_log(text, log_file):
    """Prints the text to the console and logs it to the file."""
    print(text)
    if log_file:
        log_file.write(text + "\n")

def main():
    """
    Main function to parse arguments and start the directory tree printing, logging to a file.
    """
    # Set default values
    start_path = None
    max_depth = None

    # Use sys.argv to get the command-line arguments
    if len(sys.argv) > 1:
        start_path = sys.argv[1]  # Get the directory path from the first argument
        
        # Check if a depth limit was provided
        if len(sys.argv) > 2:
            try:
                max_depth = int(sys.argv[2])
                print(f"Depth limit set to: {max_depth}")
            except ValueError:
                print(f"Warning: Invalid depth limit '{sys.argv[2]}'. Using no limit.")
        
        continue_script(start_path, max_depth)
    else:
        print("Default relative directory logging is disabled due to caution")

def continue_script(start_path, max_depth=None):
    log_file_path = "tree_log.txt"

    try:
        with open(log_file_path, "w", encoding="utf-8") as log_file:  # Specify encoding here
            if not os.path.exists(start_path):
                line = f"Error: The path '{start_path}' does not exist."
                print_and_log(line, log_file)
                return

            if not os.path.isdir(start_path):
                line = f"Error: '{start_path}' is not a directory."
                print_and_log(line, log_file)
                return

            line = os.path.basename(start_path) + "/"  # Print the root directory name
            print(f"Attempting to access directory tree starting at: '{start_path}'")
            if max_depth is not None:
                print(f"With maximum depth of: {max_depth}")
            print_and_log(line, log_file)
            print_directory_tree(start_path, log_file=log_file, max_depth=max_depth)
            print(f"Tree logged to: {os.path.abspath(log_file_path)}")

    except Exception as e:
        print(f"Error opening or writing to log file: {e}")

if __name__ == "__main__":
    main()
