import constants as c
import utils
import os
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import networkx as nx

def read_full_line(line: str) -> tuple[str, str, list[str], int]:
    lst = line.split(",")
    devops_file_path = lst[0]
    namespace = lst[1]
    n_lines = int(lst[-1]) # the last element is the number of lines
    usings: list[str] = []
    for i in range(2, len(lst)-1): # -1 because the last element is the number of lines
        if lst[i] == "" or lst[i] == "\n":
            continue
        usings.append(lst[i])
    return devops_file_path, namespace, usings, n_lines

def normalize(nodes: list)-> mcolors.Normalize:
    
    return plt.Normalize(
        vmin=min(nodes),
        vmax=max(nodes))
def create_normalizer(nodes: list)-> mcolors.Normalize:
    return plt.Normalize(
        vmin=min(nodes),
        vmax=max(nodes))

def use_normalizer(normalizer: mcolors.Normalize, value: int)-> int:
    return normalizer(value) # Normalize the value to a range of 0-255

def read_line(line: str) -> tuple[str, str, list[str]]:
    lst = line.split(",")
    devops_file_path = lst[0]
    namespace = lst[1]
    usings: list[str] = []
    for i in range(2, len(lst)-1): # -1 because the last element is the number of lines
        if lst[i] == "" or lst[i] == "\n":
            continue
        usings.append(lst[i])
    return devops_file_path, namespace, usings

def clean_using_line(line: str):

    if line.startswith("using") or line.startswith(c.BOM_CHARACTER):
        
        without_bom = line.replace(c.BOM_CHARACTER, "").strip()
        without_global = without_bom.replace("global", "").strip()
        without_using = without_global.replace("using", "").strip()
        return without_using
    
    return None 


def split_content_into_lines(content:str) -> list[str]:
    # Split
    splitted = content.split(sep='\n')
    # The first line of the file is a BOM (ï»¿) character in some cases
    splitted[0] = splitted[0].replace(c.BOM_CHARACTER, '') 
    return splitted

def get_all_csharp_files(url: str, azure_pat: str) -> list[str]:
    
    response = utils.make_reqest(url, azure_pat, params=c.ALL_FILES_PARAMS)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch files from Azure DevOps API. Status code: {response.status_code}")
    
    all_files_json = response.json() # this return a json with "count: 0" and "value: [...]"
    all_files_in_repo = all_files_json["value"]
    csharp_files = [file for file in all_files_in_repo if do_include_file(file["path"])]
    return csharp_files

def do_include_file(file_path: str) -> bool:
    
    # if any of the files in the path is in the list of files not to include, return False
    for file_not_to_include in c.FILES_NOT_TO_INCLUDE:
        if file_not_to_include in file_path:
            return False
    
    return file_path.endswith(".cs")

def get_using_in_file(file_content: str) -> tuple[str, list[str]]:
    """
    Summary:
    -------
    Get all using statements in a file.
    It is asumed that all the using statements are at the beginning of the file.
    
    :param file_content: The content of the file
    :return: A list of using statements
    """
    lines = split_content_into_lines(file_content)
    using_lines = []
    namespace = None
    for line in lines:
        if is_using_line(line):
            using_lines.append(line)
        if is_line_namespace(line):
            namespace = line
    return namespace, using_lines

def get_using_line_only(line: str) -> str:
    """
    Summary:
    -------
    This method handles when the using statement contains '='
    e.g line = "using Calculation = Common.Base.Calculation;" 
    
    :param line: The line to get the using line from
    :return: The using line only ("Common.Base.Calculation")
    """
    if not "=" in line:
        return line # Do nothing to the line
    
    splitted = line.split("=") # Split the line into two parts
    return splitted[-1].strip() # Return the second part of the line (the using statement)

def clean_using_line(line: str):
    
    if not "using" in line:
        return None 

    if line.startswith(c.BOM_CHARACTER):
        line = line.replace(c.BOM_CHARACTER, "").strip()

    if "=" in line:
        line = get_using_line_only(line)   
        
    without_bom = line.replace(c.BOM_CHARACTER, "").strip()
    without_global = without_bom.replace("global", "").strip()
    without_static = without_global.replace("static", "").strip()
    without_using = without_static.replace("using", "").strip()
    without_semicolon = without_using.replace(";", "").strip()
    return without_semicolon
    

def clean_namespace_line(line: str)-> str:
    if not line.startswith("namespace") and not line.startswith("global namespace"):
        return None
    without_namespace = line.replace("namespace", "").strip()
    without_global = without_namespace.replace("global", "").strip()
    without_braces = without_global.replace("{", "").strip()
    without_semicolon = without_braces.replace(";", "").strip()
    return without_semicolon

def get_normalized(G: nx.DiGraph)-> tuple[list, mcolors.Normalize, list, mcolors.Normalize]:
     # Separate nodes by type
    namespace_nodes = [node for node, attr in G.nodes(data=True) if attr['type'] == "namespace"]
    file_nodes = [node for node, attr in G.nodes(data=True) if attr['type'] == "file"]

    # Get the in-degree and out-degree values for the nodes
    data_in_degree_namespace = [G.in_degree(node) for node in namespace_nodes]
    data_out_degree_filenames = [G.out_degree(node) for node in file_nodes]
        
    norm_namespace = plt.Normalize(
        vmin=min(data_in_degree_namespace),
        vmax=max(data_in_degree_namespace))

    norm_filenames = plt.Normalize(
        vmin=min(data_out_degree_filenames),
        vmax=max(data_out_degree_filenames))
    
    return data_out_degree_filenames, norm_filenames, data_in_degree_namespace, norm_namespace



def get_all_usings_in_file(file_content: str) -> tuple[str, list[str]]:
    """
    Summary:
    -------
    Get all using statements in a file.
    It is asumed that all the using statements are at the beginning of the file.
    
    :param file_content: The content of the file
    :return: A tuple of (namespace, A list of using statements)
    """
    lines = split_content_into_lines(file_content)
    using_lines = []
    namespace = None
    for line in lines:
        if is_using_line(line):
            clean = clean_using_line(line)
            using_lines.append(clean)
        if is_line_namespace(line):
            namespace = clean_namespace_line(line)
            break # we only want the first namespace
    
    return namespace, using_lines

def save_usings_to_file(all_csharp_files: list, azure_pat: str) -> None:
    """
    Summary:
    -------
    Save all the usings in a file (usings.txt). 
    
    Parameters:
    ----------
    all_csharp_files: list of all csharp files in the repo
    azure_pat: Azure personal access token to access the repo
    """
    # Make data directory if it does not exist
    if not os.path.exists(c.DATA_DIRECTORY_PATH):
        os.makedirs(c.DATA_DIRECTORY_PATH)
        print(f"Created directory: {c.DATA_DIRECTORY_PATH}")

    # Create usings.txt file where each row is a file name and the usings in that file
    if os.path.exists(c.USINGS_TXT_FILE_PATH):
        os.remove(c.USINGS_TXT_FILE_PATH)
        print(f"{c.USINGS_TXT_FILE_PATH} already exists. Deleted it.")

    if os.path.exists('files_not_fectched.txt'):
        os.remove('files_not_fectched.txt')
        print("files_not_fectched.txt already exists. Deleted it.")

    for file in all_csharp_files:
        file_url = file['url']
        
        try: # Try to fetch the file content
            file_content_response = utils.make_reqest(file_url, azure_pat)
        except: # if the request fails, we will not stop the program
            print(f"Failed to fetch file content: {file_url}")
            with open('files_not_fectched.txt', 'a') as f:
                f.write(file_url)
            continue
        
        if file_content_response.status_code != 200:
            print(f"Failed to fetch file content: {file_url}")
            with open('files_not_fectched.txt', 'a') as f:
                f.write(file_url)
            continue
        

        namespace, all_usings_in_file = get_all_usings_in_file(file_content_response.text)
        if namespace is None:
            print(f"Namespace not found in file: {file_url}")
            continue

        n_lines = utils.get_number_of_line(file_content_response.text)
        # Open txt file where each row is a file name 
        with open(c.USINGS_TXT_FILE_PATH, 'a') as f:
            f.write(file_url)
            f.write(",")
            f.write(namespace)
            f.write(",")
            for using in all_usings_in_file:
                if using is None:
                    continue
                f.write(using)
                f.write(",")
            f.write(str(n_lines))

            f.write("\n")
    
    print(f"Saved usings in file: {c.USINGS_TXT_FILE_PATH}")


### Helper functions ###
def abstract(namespace):

    splitted = namespace.split(".")
    output_len = len(splitted) - 1
    if output_len == 0 or output_len == 1:
        return namespace

    return ".".join(splitted[:output_len]) 

def get_class_name(file_path: str) -> tuple[str, str]:
    splitted = file_path.split("/")
    file = splitted[-1]
    namespace = ".".join(splitted[1:-1])
    class_name = file.split(".")
    return namespace, class_name[0]

def get_project_from_using(using: str):
    splitted = using.split(".")
    one_two = splitted[0] + "." + splitted[1]
    one_two_tree = None
    if len(splitted) >= 3 :
        one_two_tree = one_two + "." + splitted[2]
    
    if one_two_tree is not None and one_two_tree in c.ALL_PROJECTS:
        return one_two_tree
    
    if one_two in c.ALL_PROJECTS:
        return one_two
    
    return None
def split_content_into_line(content:str) -> list[str]:
    return content.split(sep='\n')

def ignore_using(using_line: str) -> bool:
    for using_not_to_include in c.USINGS_NOT_TO_INCLUDE:
        # This could be 'System' - and would filter out all System.* usings
        if using_not_to_include in using_line:
            return True
        
    for using_to_include in c.EXTERNAL_USINGS:
        # This could be 'System' - and would filter out all System.* usings
        if using_to_include in using_line:
            return True
        
    return False

def is_line_namespace(line: str):
    if line.startswith("//"): # then the line is a comment
        return False

    if line.startswith("#"): # then the line is a preprocessor directive
        return False

    return line.startswith("namespace") or line.startswith("global namespace")

def is_using_line(line: str):
    if line.startswith("//"): # then the line is a comment
        return False

    if line.startswith("#"): # then the line is a preprocessor directive
        return False

    return line.startswith("using") or line.startswith("global using")


def get_cyclomatic_complexity(df, namespace:str, class_name: str) -> int:
    cc = 0
    # Get the cyclomatic complexity for the class name 
    rows = df[df["Type"] == class_name]
    if len(rows) == 0:
        print(f"Class {class_name} not found in the metrics file.")
        return cc
    if len(rows) == 1:
        cc = int(rows["Cyclomatic Complexity"].values[0])
    else:
        filtered_rows = rows[rows["Namespace"] == namespace]
        if len(filtered_rows) == 0:
            print(f"Namespace {namespace} not found in the metrics file.")
            return cc
        cc = int(filtered_rows["Cyclomatic Complexity"].values[0])
    
    return cc

