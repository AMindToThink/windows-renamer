# Script that renames all files in a directory to remove windows illegal characters
# While doing so, it creates a dictionary with the old and new names
# It then goes through all .r, .R, .py and .ipynb files in the directory and replaces the old names with the new names
import os
import re
import argparse
# Get current directory
directory = os.getcwd()
# List of windows illegal characters
illegal_chars = r'<>:"/\|?*'
# This one resulted in filenames that were too long. illegal_char_to_legal_char_dict = {'<':'[lt]','>':'[gt]',':':'[colon]','"':'[quote]','/':'[fslash]','\\':'[bslash]','|':'[pipe]','?':'[question]','*':'[star]'}

# Can use regular expression r'\[...\]' and r'\[..\]' to find what got changed. Handy!
illegal_char_to_legal_char_dict = {'<':'[lt]','>':'[gt]',':':'[col]','"':'[quo]','/':'[fsl]','\\':'[bsl]','|':'[pip]','?':'[que]','*':'[sta]'}
legal_char_to_illegal_char_dict = {v:k for k,v in illegal_char_to_legal_char_dict.items()}


# Note: There are no < or > in the file names.
# : does appear in the file names
# " does appear in the file names just once (triplicated, though)
# / can't be used in mac file names either
# \ Can't be used in mac file names either
# | appears in the file names
# ? appears in the file names
# * appears in the file names

def dict_replace(dictionary):
    def replace(name:str):
        for key, value in dictionary.items():
            name = name.replace(key, value)
        return name
    return replace
fix_name = dict_replace(illegal_char_to_legal_char_dict)
unfix_name = dict_replace(legal_char_to_illegal_char_dict)

extensions_to_change = ['.r','.R','.py','.ipynb']
def is_change_file(filename:str):
    return any((filename.endswith(ext) for ext in extensions_to_change))

str_to_func = {'fix':fix_name, 'unfix':unfix_name}

# Function to rename files
def rename_and_internally_replace_files(directory, direction_function, dry_run=True):
    assert direction_function in [fix_name, unfix_name]
    # Give the user a warning and make them confirm
    print(f"Renaming files in {directory}")
    print("Are you sure you want to continue? (y/n)")
    response = input()
    if response != 'y':
        print("Exiting...")
        return
    
    old_to_new_dict : dict[str,str] = {}
    def rename_files(directory, direction_function):
        for filename in os.listdir(directory):
            # If the file is a directory, call the function recursively
            filepath = os.path.join(directory,filename)
            if os.path.isdir(filepath):
                rename_files(filepath, direction_function)
            # Rename files and folders
            new_filename = direction_function(filename)
            if new_filename == filename:
                continue
            print(f"Renaming {filename} to {new_filename}")
            old_to_new_dict[filename] = new_filename
            new_filepath = os.path.join(directory,new_filename)
            if not dry_run:
                os.rename(filepath, new_filepath)
    
    rename_files(directory, direction_function)
    def replace_in_files(directory, old_to_new_dict):
        # Replace old names with new names in all .r, .py and .ipynb files
        
        for filename in os.listdir(directory):
            filepath = os.path.join(directory,filename)
            if os.path.isdir(filepath):
                replace_in_files(filepath, old_to_new_dict)
                continue

            if not is_change_file(filename):
                continue
            
            with open(filepath, 'r') as file:
                filedata = file.read()
            newfiledata = filedata
            for old_name, new_name in old_to_new_dict.items():
                newfiledata = newfiledata.replace(old_name, new_name)

            if filedata == newfiledata:
                continue

            print(f"Replacing in {filepath}")
            if dry_run:    
                continue    

            with open(filepath, 'w') as file:
                file.write(newfiledata)

    replace_in_files(directory, old_to_new_dict)
    
    if dry_run:
        import pdb; pdb.set_trace()
        pass
    

def main():
    # Take three argument, the directory and the direction (fix or unfix), and the dry run flag
    parser = argparse.ArgumentParser(description='Rename files in a directory to remove windows illegal characters')
    parser.add_argument('directory', type=str, help='Directory to rename files in')
    parser.add_argument('direction', type=str, help='Direction to rename files in. Either fix or unfix')
    parser.add_argument('--dry-run', action='store_true', help='Dry run')
    args = parser.parse_args()
    directory = args.directory
    direction = args.direction
    dry_run = args.dry_run
    rename_and_internally_replace_files(directory, str_to_func[direction], dry_run)

if __name__ == "__main__":
    main()

        



