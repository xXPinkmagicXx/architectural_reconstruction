import requests
from requests.auth import HTTPBasicAuth
import constants as c
import os
import matplotlib.colors as mcolors



def make_reqest(
        url: str,
        azure_pat: str,
        params: str = None,
        header: str = None) -> requests.Response:
    
    return requests.get(url, auth=HTTPBasicAuth('', azure_pat), params=params, headers=header)    


def get_items_request_url(organisation: str, project: str, repository: str) -> str:
    """
    Summary:
    -------
    Get the request URL for the Azure DevOps API.
    
    :param organisation: The organisation name
    :param project: The project name
    :param repository: The repository name
    :return: The request URL
    """
    return c.ALL_FILES_URL.format(
        organisation=organisation,
        project=project,
        repository=repository
    )



def get_module_name_from_path(file_path:str) -> str:
    without_cs = file_path.replace(".cs", "") # remove file extension
    without_dot = without_cs.replace(".", "") # Some folders have a dot in the name, so we need to remove it
    module_name = without_dot.replace("/", ".")
    return module_name.removeprefix(".")

def get_items_over(over: int, files: dict) -> dict:
    return {k: v for k, v in files.items() if v > over}

def get_tuples_over(over: int, lst: list[tuple[str]]) -> list[tuple[str]]:
    return [(k, v) for k, v in lst if v > over]

def get_file_path_from_devops_url(devops_url: str) -> str:
    params_dropped = devops_url.split("?")[0]
    return params_dropped.replace(c.BASE_ITEMS_URL+"/","")

def get_number_of_lines(file_content: str) -> int:
    """
    Summary:
    -------
    Get the number of lines in a file.
    
    :param file_content: The content of the file
    :return: The number of lines in the file
    """
    lines = file_content.splitlines()
    return len(lines)


# if run as main module
def main():
    print("This is a utility module.")

if __name__ == "__main__":
    main()
