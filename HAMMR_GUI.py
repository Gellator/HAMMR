import customtkinter as ctk
from tkinter import filedialog, IntVar
from HAMMR_SupportMethods import (GetAllFilesRelatedToMethod,SetMethodLibrariesToLocalVersion,CopyFileToLocation,
                                  SetMethodLibrariesToRepoVersion,SetMethodLayoutToLocalLayout,GetFoldersInDir)
from HAMMR_CheckSumConstructor import SetFilesToAddCheckSum

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.File_to_Convert = ""
        self.Robot_dict = {}
        self.FilesToMove = []
        self.fileDonor = ""
        self.title("HAMMR")
        self.geometry(f"{1100}x{580}")
        self.grid_columnconfigure((1), weight=1)
        self.grid_columnconfigure(( 2 ,3, 4, 5), weight=0)
        self.grid_rowconfigure((0), weight=0)
        self.grid_rowconfigure(( 1, 2, 3, 4), weight=1)

        self.center_label = ctk.CTkLabel(master=self, text="Hamilton Automation Method Manager Repository", font=("DM Sans", 24), compound="center", anchor="center")
        self.center_label.grid(row=0, column=0, columnspan=4, pady=15)

        #region create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=1, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Process Selection", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = ctk.CTkButton(master= self.sidebar_frame, text="Convert Method to local Libraries", command=lambda :self.SelectPage(self.sidebar_button_1, self.ConvertMethodToRepoLibrariesPage))
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, text="Deploy Method to Fleet", command=lambda :self.SelectPage(self.sidebar_button_2, self.DeployMethodPage))
        self.sidebar_button_2.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_3 = ctk.CTkButton(self.sidebar_frame, text="Convert Method to Repo Libraries", command=lambda :self.SelectPage(self.sidebar_button_3, self.ConvertMethodToRepoLibrariesPage))
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        print(self.sidebar_button_1._fg_color)
        #endregion    
        self.center_frame = ctk.CTkFrame(master=self,fg_color="transparent")
        self.center_frame.grid(row=1, column=1, rowspan=4, columnspan=3, padx=(20, 20), pady=(0, 0), sticky="nsew")
        self.center_frame.grid_rowconfigure(4, weight=1)
        self.center_frame.grid_columnconfigure([1,2,3,4], weight=1)    

    #region Page Constructors
    def SelectPage(self,btn, page):
        self.DeselectPageButtons()
        self.Delete_Pages()
        btn.configure(fg_color="blue")
        page()
    def DeselectPageButtons(self):
        self.sidebar_button_1.configure(fg_color="#2FA572")
        self.sidebar_button_2.configure(fg_color="#2FA572")
        self.sidebar_button_3.configure(fg_color="#2FA572")
    def HomePage(self):
        self.center_HomePage = ctk.CTkFrame(master=self.center_frame)
        self.center_HomePage.grid(row=1, column=1, rowspan=4, columnspan=3, padx=(20, 20), pady=(0, 0), sticky="nsew")
        self.center_HomePage.grid_rowconfigure(4, weight=1) 
        self.HomeLabel = ctk.CTkLabel(master=self.center_HomePage, text="Welcome", font=("DM Sans", 24))
        self.HomeLabel.grid(row=1, column=1,columnspan=3, padx=20, pady=20)
    def ConvertMethodToLocalLibrariesPage(self):
        self.center_ToLocalLibrariesPage = ctk.CTkFrame(master=self.center_frame)
        self.center_ToLocalLibrariesPage.grid(row=1, column=1, rowspan=4, columnspan=3, padx=(20, 20), pady=(0, 0), sticky="nsew")
        self.ToLocalLibrariesPageLabel = ctk.CTkLabel(master=self.center_ToLocalLibrariesPage, text="Welcome", font=("DM Sans", 24))
        self.ToLocalLibrariesPageLabel.grid(row=1, column=1,columnspan=3, padx=20, pady=20)
        self.center_ToLocalLibrariesPageConfirmButton = ctk.CTkButton(master=self.center_ToLocalLibrariesPage, text="Confirm", command=self.ConvertToLocalLibraries, width=200, height=40, font=("DM Sans", 24))
        self.center_ToLocalLibrariesPageConfirmButton.grid(row=3, column=1, columnspan=4, padx=20, pady=20)
        self.center_ToLocalLibrariesPageConfirmButton.configure(state = "disabled")
        self.center_ToLocalLibrariesPageDonorPathLabel = ctk.CTkLabel(master=self.center_ToLocalLibrariesPage, text=" None Selected", font=("DM Sans", 24), text_color= "red")
        self.center_ToLocalLibrariesPageDonorPathLabel.grid(row=1, column=3, padx=10, pady=20)
        self.center_ToLocalLibrariesPageSelectMethodButton = ctk.CTkButton(master=self.center_ToLocalLibrariesPage, text="Select Method", command=lambda :self.GetMethodForConvert(self.center_ToLocalLibrariesPageConfirmButton,self.center_ToLocalLibrariesPageDonorPathLabel), width=200, height=40, font=("DM Sans", 24))
        self.center_ToLocalLibrariesPageSelectMethodButton.grid(row=2, column=1, columnspan=4, padx=20, pady=20)
    def ConvertMethodToRepoLibrariesPage(self):
        self.center_MethodToRepoLibrariesPage = ctk.CTkFrame(master=self.center_frame)
        self.center_MethodToRepoLibrariesPage.grid(row=1, column=1, rowspan=4, columnspan=3, padx=(20, 20), pady=(0, 0), sticky="nsew")
        self.center_MethodToRepoLibrariesPageLabel = ctk.CTkLabel(master=self.center_MethodToRepoLibrariesPage, text="Welcome", font=("DM Sans", 24))
        self.center_MethodToRepoLibrariesPageLabel.grid(row=1, column=1,columnspan=3, padx=20, pady=20)
        self.center_MethodToRepoLibrariesPageSelectMethodButton = ctk.CTkButton(master=self.center_MethodToRepoLibrariesPage, text="Select Method", command=lambda :self.GetMethodForConvert(self.center_MethodToRepoLibrariesPageConfirmButton,self.center_MethodToRepoLibrariesPageDonorPathLabel), width=200, height=40, font=("DM Sans", 24))
        self.center_MethodToRepoLibrariesPageSelectMethodButton.grid(row=2, column=1, columnspan=4, padx=20, pady=20)
        self.center_MethodToRepoLibrariesPageDonorPathLabel = ctk.CTkLabel(master=self.center_MethodToRepoLibrariesPage, text=" None Selected", font=("DM Sans", 24), text_color= "red")
        self.center_MethodToRepoLibrariesPageDonorPathLabel.grid(row=1, column=3, padx=10, pady=20)
        self.center_MethodToRepoLibrariesPageConfirmButton = ctk.CTkButton(master=self.center_MethodToRepoLibrariesPage, text="Confirm", command=self.ConvertToRepoLibraries, width=200, height=40, font=("DM Sans", 24))
        self.center_MethodToRepoLibrariesPageConfirmButton.grid(row=3, column=1, columnspan=4, padx=20, pady=20)
        self.center_MethodToRepoLibrariesPageConfirmButton.configure(state = "disabled") 
    def DeployMethodPage(self):
        self.center_DeployMethodPage = ctk.CTkFrame(master=self.center_frame)
        self.center_DeployMethodPage.grid(row=1, column=1, rowspan=4, columnspan=3, padx=(20, 20), pady=(0, 0), sticky="nsew")
        self.center_DonorPathtitle = ctk.CTkLabel(master=self.center_DeployMethodPage, text="Method to deploy:", font=("DM Sans", 24))
        self.center_DonorPathtitle.grid(row=1, column=1,columnspan=2, padx=20, pady=20)
        self.center_DonorPathLabel = ctk.CTkLabel(master=self.center_DeployMethodPage, text=" None Selected", font=("DM Sans", 24), text_color= "red")
        self.center_DonorPathLabel.grid(row=1, column=3, padx=10, pady=20)
        self.center_SelectMethodButton = ctk.CTkButton(master=self.center_DeployMethodPage, text="Select Method", command=self.GetMethodFiles, width=200, height=40, font=("DM Sans", 24))
        self.center_SelectMethodButton.grid(row=2, column=1, columnspan=2, padx=20, pady=20)
        self.center_SelectDeploymentButton = ctk.CTkButton(master=self.center_DeployMethodPage, text="Deploy to selected sites", command=self.DeployMethodToSelectedRobots)
        self.center_SelectDeploymentButton.grid(row=5, column=1, columnspan=2, padx=20, pady=20)
        self.center_SelectDeploymentButton.configure(state="disabled")
        self.checkbox_slider_frame = ctk.CTkFrame(master=self.center_DeployMethodPage)
        self.checkbox_slider_frame.grid(row=4, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.CreateCheckBoxPerDestination(self.checkbox_slider_frame)
    def Delete_Pages(self):
        for frame in self.center_frame.winfo_children():
            frame.destroy()
    #endregion

    #region App Functions
    # really need to abstract this out to clean up code base -SG
    def DeployMethodToSelectedRobots(self):
        _filesToCheckSum = ""
        multi = False
        for key, value in self.Robot_dict.items():
            if value.get():
                prefix ="C:\Program Files (x86)\HAMILTON\Repo\ProDevHamilton/"
                MethodDestination = prefix + key +'/Methods'
                layoutFolder =  prefix + key +'/Layouts'
                for i in range(len(self.FilesToMove)):
                    file = CopyFileToLocation(self.FilesToMove[i], MethodDestination)
                    if i == 0: # the first file is always teh .HSL file since it is appended first see GetMethodFiles() -SG
                        SetMethodLayoutToLocalLayout(file, layoutFolder)
                        hslFile = file
                if multi:
                    _filesToCheckSum = _filesToCheckSum +";"+ hslFile
                else:
                    _filesToCheckSum = _filesToCheckSum + hslFile
                if hslFile:
                    multi = True
        self.center_SelectDeploymentButton.configure(state="disabled")
        self.center_DonorPathLabel._text = "Method has been deployed Continue with Checksum"
        self.FilesToMove = [] 
        SetFilesToAddCheckSum(_filesToCheckSum)
        #PyHamilton_AddMultipleCheckSums(_filesToCheckSum)
    def CreateCheckBoxPerDestination(self, masterframe):
        folders = GetFoldersInDir("C:\Program Files (x86)\HAMILTON\Repo\ProDevHamilton")
        for folder in folders:
            self.Robot_dict[folder] =0
        for i,key in enumerate(self.Robot_dict,1):
            self.Robot_dict[key] = IntVar()
            e = ctk.CTkCheckBox(master=masterframe, text=key, variable=self.Robot_dict[key])
            e.grid(row=i, column=0, pady=(20, 20), padx=20, sticky="nwe") 
    def GetMethodForConvert(self, ConfirmButton,Label): 
        input_file_Raw = filedialog.askopenfile(title='Select input file', filetypes=(('HSL Files', '*.hsl'),))
        if not input_file_Raw:
            print('No input file selected. Exiting...')
            ConfirmButton.configure(state = "disabled")
            return
        else:
            self.File_to_Convert = input_file_Raw.name
            Label.configure(text= input_file_Raw.name)
            ConfirmButton.configure( state="enabled")  
    def ConvertToLocalLibraries(self):
        self.center_ToLocalLibrariesPageConfirmButton.configure(state = "disabled")
        output = "Selected method has been converted to local libraries please select a new method "
        self.center_ToLocalLibrariesPageDonorPathLabel.configure(text= output) 
        SetMethodLibrariesToLocalVersion(self.File_to_Convert) 
        SetFilesToAddCheckSum(self.File_to_Convert)
        #PyHamilton_AddMultipleCheckSums(self.File_to_Convert)
        self.File_to_Convert = ""
    def ConvertToRepoLibraries(self):
        self.center_MethodToRepoLibrariesPageConfirmButton.configure(state = "disabled")
        output = "Selected method has been converted to repo libraries please select a new method "
        self.center_MethodToRepoLibrariesPageDonorPathLabel.configure(text= output)
        SetMethodLibrariesToRepoVersion(self.File_to_Convert) 
        SetFilesToAddCheckSum(self.File_to_Convert)
        #PyHamilton_AddMultipleCheckSums(self.File_to_Convert) 
        self.File_to_Convert = ""
    def GetMethodFiles(self):
        input_file_Raw = filedialog.askopenfile(title='Select input file', filetypes=(('HSL Files', '*.hsl'), ('All Files', '*.*')))
        if not input_file_Raw:
            return
        else:
            input_file = input_file_Raw.name
        self.FilesToMove = GetAllFilesRelatedToMethod(input_file)
        _foundAllFiles = (len(self.FilesToMove) == 4)
        if _foundAllFiles:
            self.center_SelectDeploymentButton.configure(state="enabled")
            self.center_DonorPathLabel.configure(text = input_file, font = ("DM Sans", 12), text_color= "white")
        else:
            self.center_SelectDeploymentButton.configure(state="disabled")
            self.center_DonorPathLabel._text = "Did not find all files, found: " + str(len(self.FilesToMove)) + " files"
    def GetLocation(self):
        destination_Hamilton_file = filedialog.askdirectory(title='Select Hamilton to deploy to', mustexist=True)
        if not destination_Hamilton_file:
            return
        prefix = destination_Hamilton_file.split('/Methods')
        layoutFolder =  prefix[0] +'/Layouts'
        for i in range(len(self.FilesToMove)):
            file = CopyFileToLocation(self.FilesToMove[i], destination_Hamilton_file)
            if i == 0:     # The first one in the list is ALWAYS the .hsl file
                SetMethodLayoutToLocalLayout(file, layoutFolder)
                SetFilesToAddCheckSum(file)
                    
    #endregion    


if __name__ == '__main__':
    app = App()
    app.mainloop()