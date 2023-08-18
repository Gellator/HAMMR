import os
import shutil

def SetMethodLibrariesToLocalVersion(input_file):
    """Description:
        Converts the given .HSL file's library include references from current to the standard location on Hamilton install (C:\Program Files (x86)\HAMILTON\Library)
    Args:
        input_file (string): A file path to a .HSL file
    Returns:
        None
    """
    search_string = ' namespace _Method { #include "'
    with open(input_file, 'r') as file:
        lines = file.readlines()
    for line in lines:
        if line.startswith(search_string):

            if line.__contains__('HSL'):
                before = line
                right = line.split('HSL')
                print(right[1])
                final = search_string + 'HSL' + right[1]
                print(final)
            elif line.__contains__('Sequence'):
                before = line
                right = line.split('SequenceTools_V3.')
                print(right[1])
                final = search_string + 'SequenceTools_V3\\SequenceTools_V3.' + right[1]
                print(final)
            lines = [line.replace(before,final) for line in lines]
    with open(input_file, 'w') as file:
        file.writelines(lines)

def CopyFileToLocation(source_path, destination_path):
    """Description:
        Copies a singular file to a new location.
    Args:
        source_path (string): Path to the file you wish to copy.
        destination_path (string): Path to the location you want you copy to be made.
    Returns:
        None
    """
    try:
        newpath = shutil.copy2(source_path, destination_path)
        print("File copied successfully!")
        return newpath
    except FileNotFoundError:
        print("Source file not found.")
    except IsADirectoryError:
        print("Source is a directory, not a file.")
    except shutil.SameFileError:
        print("Source and destination paths are the same.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def SetMethodLibrariesToRepoVersion(input_file):
    """Description:
        Converts the given .HSL file's library include references from current to the Repo specific location (C:\Program Files (x86)\HAMILTON\Repo\ProDevHamilton\Main Development\Library\\)
    Args:
        input_file (string): A file path to a .HSL file
    Returns:
        None
    """
    exclude_list = ["HSLMETEDLib.hs_","HSLMECCLib.hs_","HSLPTLLib.hsl","HSLSTCCLib.hs_" ] # Must exclude these as modifying these messes with deeper layers of C++ code to reference files.
    search_string = 'namespace _Method { #include "'
    with open(input_file, 'r') as file:
        lines = file.readlines()
              
    updated_lines = [line.replace('namespace _Method { #include "', 'namespace _Method { #include "C:\Program Files (x86)\HAMILTON\Repo\ProDevHamilton\Main Development\Library\\') for line in lines if not any(exclude_str in line for exclude_str in exclude_list)]               
    with open(input_file, 'w') as file:
        file.writelines(updated_lines)

def SetMethodLayoutToLocalLayout(input_file, LayoutFolder):
    """Description:
        Converts the .HSL reference for both .Lay and .Res to the version in the given layout folder
    Args:
        input_file (string): What .HSL file to convert
        LayoutFolder (string): The name of the hamilton robot folder the new layout .Lay and .Res file exist (NOT the PATH, EX: "Ham-08 Mothra")
    Returns:
        None 
    """
    pre = 'global device ML_STAR ("'
    pre2 = '#include "'
    before = ''
    before2 = ''
    final=''
    final2=''
    with open(input_file, 'r') as file:
            lines = file.readlines()
    for line in lines:
        if line.startswith('global') and line.__contains__('\Layouts'):
            before = line
            right = line.split('\Layouts')
            final = pre + LayoutFolder + right[1]
            print(final)
            final = final.replace('/','\\')
            print(final)
        if line.startswith('#include "C:\Program Files (x86)\HAMILTON'):
            before2 = line
            right = line.split('\Layouts')
            final2 = pre2 + LayoutFolder + right[1]
            print(final2)
            final2 = final2.replace('/','\\')
            print(final2)
    lines = [line.replace(before,final) for line in lines]
    lines = [line.replace(before2,final2) for line in lines]
    with open(input_file, 'w') as file:
        file.writelines(lines)  

def GetFoldersInDir(directoryPath):
    """Description:
        Helper function to grab all available folders within a location excluding the .git folder.
    Args:
        directoryPath (string): The path of the directory to search.
    Returns:
        folderNames (list[string]): A list of strings of the names of each folder found.
    """
    folderNames=[] 
    for item in os.listdir(directoryPath):
        itemPath= os.path.join(directoryPath, item)
        if os.path.isdir(itemPath):
            if item != ".git":
                folderNames.append(item)
    return folderNames      

def GetHSLFileInDeploymentLocation(FilesToMove, folder):
    """Description:
        WARnING: Combination of both CopyFileToLocation and SetMethodLayoutToLocalLayout :WARNING
        Creates a destination location depending on given folder and copies all files in FilesToMove to this location along with setting the layout of the .HSL file to that destinations version.
    Args:
        FilesToMove (List[string]): A list of file paths to be copied to a location. The FilesToMove[0] must be the .HSL file.
        folder (string): The Hamilton Robot repo folder location (EX: "Ham-08 Mothra").
    Returns:
        forcheck (string): A filepath to the newly created and edited .HSL file.
    """
    prefix ="C:\Program Files (x86)\HAMILTON\Repo\ProDevHamilton/"
    MethodDestination = prefix + folder +'/Methods'
    layoutFolder =  prefix + folder +'/Layouts'            
    for i in range(len(FilesToMove)):
        file = CopyFileToLocation(FilesToMove[i], MethodDestination)
        if i == 0:
            SetMethodLayoutToLocalLayout(file, layoutFolder)
            forcheck = file
        
        return forcheck

def GetAllFilesRelatedToMethod(input_file):
    """Description:
        Searches the given input_files location for files that share the same name but different types
    Args:
        input_file (string): File path to the .HSL file for a method
    Returns:
        _relatedFiles (list[string]): A list of file paths that share the same name but different type as input_file.
    """
    _relatedFiles = []
    directory, filename = os.path.split(input_file)
    file_name, file_extension = os.path.splitext(filename)
    _relatedFiles.append(input_file)
    for root, dirs, files in os.walk(directory):
        for file in files:
            name, extension = os.path.splitext(file)
            if file_name in file and extension != file_extension:
                temp = os.path.join(root,file)
                temp.replace('\\', '/')
                _relatedFiles.append(temp)
    return _relatedFiles