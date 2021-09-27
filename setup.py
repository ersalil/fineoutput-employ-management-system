import cx_Freeze
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"
shortcut_table = [
    ("DesktopShortcut",  # Shortcut
     "DesktopFolder",  # Directory_
     "fine output",  # Name
     "TARGETDIR",  # Component_
     "[TARGETDIR]\main.exe",  # Target
     None,  # Arguments
     None,  # Description
     None,  # Hotkey
     None,  # Icon
     None,  # IconIndex
     None,  # ShowCmd
     "TARGETDIR",  # WkDir
     )
]
msi_data = {"Shortcut": shortcut_table}

# Change some default MSI options and specify the use of the above defined tables
bdist_msi_options = {'data': msi_data}

executables = [cx_Freeze.Executable(script="main.py", icon='cc.ico', base=base)]

cx_Freeze.setup(
    version="1.0",
    description="Fine Oput",
    author="vedjangid",
    name="main.py",

    options={"build_exe": {"packages": [ "numpy", "cv2", "PIL", "pynput", "win32api", "pyqt5",
                                        "pytz", "scapy", "winpcapy", "sqlite3",
                                        "requests"],
                           "include_files": ['refresh.png','screen.png', 'setting.png', 'home.png', 'task.png',
                                                                                                            'add.png',
                                             'attendence.png', 'menu.png', 'ui_functions.py','logosplash.png',
                                             'python_software_disable_script.py', 'python_usb_enable_script.py',
                                             'cc.ico', 'login.ui', 'side_bar - Copy - Copy.ui', 'nav_button_css.py',
                                             'logo.png', 'fineoutput.png', 'enimation_splash.gif','login_splash.ui',
                                             'ip_dialog.ui','task_add.ui','setting_dialog.ui','connected_ip.py',
                                             'attendence_start_dialog.ui','attendence_stop_dialog.ui',
                                             'logout_dialog.ui','task_complete_dialog.ui',
                                             'task_create_successfully_2.ui','side_bar - Copy.ui',
                                             'attendence_start_dialog_after_responce.ui',
                                             'attendence_stop_dialog_after_responce.ui',
                                             'circular_loader.ui','task_add - Copy.ui',
                                             'task_complete_dialog_after_responce.ui','new_loader.ui'
                                             ]},
             "bdist_msi": bdist_msi_options,
             },
    executables=executables

)

# C:\Users\VED\AppData\Local\Programs\main.py\
# "cachetools", "certifi", "chardet", "future", "idna","pefile","shiboken2","urllib3", "six"