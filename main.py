import argparse
import os
import fnmatch
import re

# Create an ArgumentParser object
parser = argparse.ArgumentParser()

# Add command-line arguments
parser.add_argument("--path", required=True, help="The path to the directory")
parser.add_argument("--excludeFolders", default="", help="Semicolon-separated list of folders to exclude")
parser.add_argument("--excludeFiles", default="", help="Semicolon-separated list of files to exclude")
parser.add_argument('--onlyTree', action='store_true', help="print file structure only")

# defaults
DEFAULT_EXCLUDE_FOLDERS = []
DEFAULT_EXCLUDE_FILES = []
with open('default_excludes.txt', 'r') as f:
    raw_folders, raw_files = f.read().split('---')
    DEFAULT_EXCLUDE_FOLDERS = raw_folders.split('\n')
    DEFAULT_EXCLUDE_FILES = raw_files.split('\n')
STARTING_MESSAGE = "You will be my developer assistant. I'm going to provide you with all the information about my codebase and your job is to help me understand it. After I provide all the information, you will respond to me by very briefly summarizing the technology and tech stack used. Then I will ask you further questions.\n"

# Parse the command-line arguments
args = parser.parse_args()

def getFileStructure(path, excludeFolders=[], excludeFiles=[]):
    # Create an empty list to store the directory structure
    structure = []

    # Recursively iterate over all files and directories under the specified path
    for root, dirs, files in os.walk(path):
        # Exclude any folders or files that match the specified exclusions
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in excludeFolders)]
        files = [f for f in files if not any(fnmatch.fnmatch(f, pattern) for pattern in excludeFiles)]

        # Add the current directory to the structure list
        indent_level = root.count(os.sep) - path.count(os.sep)
        structure.append("{}{}/".format("| " * indent_level, os.path.basename(root)))

        # Add each file in the current directory to the structure list
        for file in files:
            indent_level = root.count(os.sep) - path.count(os.sep) + 1
            structure.append("{}{}".format("| " * indent_level, file))

    # Return the directory structure as a formatted string
    return "\n".join(structure)

def getFileAbsPaths(path, excludeFolders=[], excludeFiles=[]):
    # Create an empty list to store the file paths
    file_paths = []

    # Recursively iterate over all files and directories under the specified path
    for root, dirs, files in os.walk(path):
        # Exclude any folders that match the specified exclusions
        # dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(os.path.join(root, d), pattern) for pattern in excludeFolders)]
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(os.path.join(root, d), pattern) or (d == pattern) for pattern in excludeFolders)]

        # Exclude any files that match the specified exclusions
        for file in files:
            if any(fnmatch.fnmatch(file, pattern) for pattern in excludeFiles):
                continue

            # # Check if the full path matches one of the excluded folders
            full_path = os.path.join(root, file)
            # if any(fnmatch.fnmatch(full_path, pattern) for pattern in excludeFolders):
            #     return ""

            # Add the absolute path of the file to the file_paths list
            file_paths.append(full_path)

    # Return the file paths list
    return file_paths

def getFileContent(root_path, filePath):
    # Read the contents of the file
    with open(filePath, "r") as file:
        print(filePath)
        content = file.read()

    # Create a string with the file path and contents
    rel_path = subtractPaths(root_path, filePath)
    return "\n{}\n{}".format(rel_path, content)

def subtractPaths(root_path, file_path):
    # Get the normalized absolute paths of the root and file paths
    root_path = os.path.abspath(root_path)
    file_path = os.path.abspath(file_path)

    # Check if the file path is a subpath of the root path
    if not file_path.startswith(root_path):
        raise ValueError("File path is not a subpath of the root path.")

    # Get the relative path of the file path from the root path
    rel_path = os.path.relpath(file_path, root_path)

    # Return the relative path
    return rel_path

if __name__ == '__main__':
    path = args.path
    excludeFolders = args.excludeFolders.split(";") if args.excludeFolders else []
    excludeFiles = args.excludeFiles.split(";") if args.excludeFiles else []
    excludeFolders += DEFAULT_EXCLUDE_FOLDERS
    excludeFiles += DEFAULT_EXCLUDE_FILES

    if not os.path.isabs(path):
        print("Error: path is not a valid absolute path")
        exit(1)

    finalString = STARTING_MESSAGE
    finalString += "Project File Structure: \n"
    fileStructure = getFileStructure(path, excludeFolders, excludeFiles)
    finalString += fileStructure

    if not args.onlyTree:
        finalString += "\n\nAll significant project files:\n"
        
        filePaths = getFileAbsPaths(path, excludeFolders, excludeFiles)
        for filePath in filePaths:
            finalString += getFileContent(path, filePath)
    
    with open('output.txt', 'w') as outputFile:
        outputFile.write(finalString)
    
    chars2token = 2.5 # openai says its 4 but for this specific usecase its more like 2.5
    tokens = len(finalString) / chars2token
    print(f'Rough estimate of number of tokens used in initial info summary: {tokens}')
