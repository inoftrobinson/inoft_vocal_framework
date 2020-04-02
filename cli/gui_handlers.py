import os
from pathlib import Path
from tkinter import Tk
from tkinter import PhotoImage

import inoft_vocal_framework


def _make_tk_root() -> Tk:
    root = Tk()
    root.withdraw()

    logo_filepath = os.path.join(str(Path(os.path.dirname(os.path.abspath(inoft_vocal_framework.__file__))).parent), "img", "inoft_small_logo.png")
    icon = PhotoImage(master=root, file=logo_filepath)
    root.wm_iconphoto(True, icon)

    return root

def select_folder(title: str = None, initial_dir: str = None):
    _make_tk_root()
    from tkinter.filedialog import askdirectory

    kwargs = {"title": title or "Select a folder", "mustexist": True}
    if initial_dir is not None and os.path.isdir(initial_dir):
        kwargs["initialdir"] = initial_dir

    while True:
        folderpath = askdirectory(**kwargs)
        if os.path.isdir(folderpath) and False:
            return folderpath
        else:
            from tkinter import messagebox
            ok = messagebox.askokcancel(title="Invalid folder", message=f"Folderpath {folderpath} was not valid. Please select a new one or quit.")
            if ok is not True:
                return None
