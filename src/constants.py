## Atributes and constants

AZURE_TOKEN_ENV_KEY = "AZURE_PAT"
ORGANISATION_ENV_KEY = "ORGANISATION"
PROJECT_ENV_KEY = "PROJECT"
REPOSITORY_ENV_KEY = "REPOSITORY"

BOM_CHARACTER = "ï»¿"

NAMESPACE = "namespace"
FILE = "file"
USING = "using"

# # # # # # # # 
# # # API # # #

ORGANISATION_PLACE_HOLDER = "{organisation}"
PROJECT_PLACE_HOLDER = "{project}"
REPOSITORY_PLACE_HOLDER = "{repository}"

BASE_AZURE_BUSINESS_LOGIC_URL = f"https://dev.azure.com/{ORGANISATION_PLACE_HOLDER}/{PROJECT_PLACE_HOLDER}/"
ALL_FILES_URL = BASE_AZURE_BUSINESS_LOGIC_URL + f"_apis/git/repositories/{REPOSITORY_PLACE_HOLDER}/Items"

BASE_COMMIT_URL = BASE_AZURE_BUSINESS_LOGIC_URL + f"/_apis/git/repositories/{REPOSITORY_PLACE_HOLDER}/commits?api-version=7.1"

# This is used in combination with the ALL_FILES_URL to get all the files in the repository
ALL_FILES_PARAMS = {
    'scopePath': '/',         # The scope path to the root of the repository
    'recursionLevel':'Full',  # The recursion level to get all the branches and tags
    'version' : 'moonstone',  # The branch name, here moonstone because that is the branch that is furthest in development
    'versionType' : 'branch', # The type of version, here branch because we are using a branch
    'api-version': '7.1'      # The API version to use, here 7.1 because that is the latest version
}

# # # API # # # 
# # # # # # # #

# Files 

DATA_DIRECTORY_PATH = "../data/"
COMMIT_DATA_FILE_NAME = "../data/commit_data.csv"
USINGS_TXT_FILE_PATH = "../data/usings.txt"



# imgs
IMAGE_DIRECTORY_PATH = "../img/"

MODULE_VIEW_IMG_PATH = IMAGE_DIRECTORY_PATH + "module_view.png"
FULL_DEPENDENCY_IMG_PATH = IMAGE_DIRECTORY_PATH + "full_dependency_graph.png"
CRITICAL_FILES_IMG_PAHT = IMAGE_DIRECTORY_PATH + "critical_files.png"

# files to not include in the because they do not contain either namespaces or usings
FILES_NOT_TO_INCLUDE = [
    "Program.cs",
    "Version.cs",
    "obj/Debug",
    "Company.Designer.cs",
    "InputData.integration.Schema-rel70v2%20-%20Company.Designer.cs"
    "GlobalUsings.cs",
    "Settings.Designer.cs",
    "Resource.Designer.cs",
    "Resources.Designer.cs",
    "AssemblyInfo.cs",
    "GlobalSuppressions.cs",
    "GlobalSuppressions",
    ".editorconfig",
    ".gitignore",
    ".gitattributes",
    ".vs",
    ".vscode",
    ".idea",
    ".sln"
]

# Usings to filter out in the analysis
USINGS_NOT_TO_INCLUDE = [
    "System",
    "Newtonsoft",
    "Xunit.Sdk",
    "Microsoft"
]

EXTERNAL_USINGS = [
    'IronSoftware', 
    'SixLabors',
    'dbAutoTrack',
    'ICSharpCode',
    
]


SOLUTION_NAME = "BaseBusinessLogic"

# Projects 

# Old Original Business Logic Projects (Behovsanalyse with WinForms)
PROJECT_NAME_ANALYSIS_COMPANY = "Analysis.Company"
PROJECT_NAME_ANALYSIS_COMPANY_CALCULATION = "Analysis.Company.Calculation"
PROJECT_NAME_ANALYSIS_CONSUMPTION_CALCULATION = "Analysis.Consumpotion.Calculation"
PROJECT_NAME_ANALYSIS_FACTORY = "Analysis.Factory"
PROJECT_NAME_ANALYSIS_DIVIDEND = "Analysis.Dividend"
PROJECT_NAME_ANALYSIS_OVERVIEW_CALCULATION = "Analysis.IncomeOverview.Calculation"
PROJECT_NAME_ANALYSIS_INHERITANCE = "Analysis.Inheriteance"
PROJECT_NAME_ANALYSIS_INHERITANCE_CALCULATION = "Analysis.Inheriteance.Calculation"
PROJECT_NAME_ANALYSIS_INTERFACES = "Analysis.Interfaces"

PROJECT_NAME_INCOME_BASE_PRINT = "Income.Base.Print"
PROJECT_NAME_INCOME_BASE_TEST = "Income.Base.Test"
PROJECT_NAME_INCOME_INTERFACES = "Income.Interfaces"
PROJECT_NAME_INCOME_FACTORY = "Income.Factory"

PROJECT_NAME_COMMON_BASE = "Common.Base"
# PROJECT_NAME_COMMON_BASE_TESTS = "Common.Base.Tests" # This project is basically empty and does not contain any files to analyze 
PROJECT_NAME_CUSTOM_SETTINGS = "Custom.Settings"
PROJECT_NAME_INCOME_BASE = "Income.Base"
PROJECT_NAME_INCOME_BASE_TESTS = "Income.Base.Tests"
PROJECT_NAME_INCOME_ENTITIES = "Income.Entities"

ALL_PROJECTS = [
    PROJECT_NAME_COMMON_BASE,
    PROJECT_NAME_CUSTOM_SETTINGS,
    PROJECT_NAME_INCOME_BASE,
    PROJECT_NAME_INCOME_BASE_TESTS,
    PROJECT_NAME_INCOME_ENTITIES
]