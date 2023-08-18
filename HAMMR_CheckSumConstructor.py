import subprocess

def SetFilesToAddCheckSum(input_files_string):
    txtHolderFilePath ='c:\Program Files (x86)\HAMILTON\Repo\ProDevHamilton\Main Development\CheckSumConstructor\Holder.txt'  
    headertitle = "filename \n"
    content = headertitle + input_files_string 
    try:
        with open(txtHolderFilePath, 'w') as file:
            file.write(content)
    except Exception as e:
        print("wtf")
    
    call_executable()
    


def call_executable():
    try:
        executable_path = 'c:\Program Files (x86)\HAMILTON\Bin\HxRun.exe'  
        input_file_path = 'c:\Program Files (x86)\HAMILTON\Repo\ProDevHamilton\Main Development\CheckSumConstructor\CheckSumConstructor.hsl'
        # Construct the command to call the executable with the input file as an argument
        command = [executable_path, input_file_path]

        # Run the command and capture the output and errors
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Print the output and errors
        print("Standard Output:")
        print(result.stdout)
        print("\nStandard Error:")
        print(result.stderr)

        # Check the return code to see if the execution was successful
        if result.returncode == 0:
            print("Execution successful!")
        else:
            print(f"Execution failed with return code {result.returncode}")
    except Exception as e:
        print(f"An error occurred: {e}")
