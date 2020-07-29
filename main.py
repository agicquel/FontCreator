from netlistParser import *
from fontUi import *
import os

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pcb = PcbParse(resource_path("./pcb.kicad_pcb"))
leds = pcb.analyse_leds()

root = tk.Tk()
root.title("Pasteur Font Creator")
root.geometry("900x800")
ui = FontUI(root, leds)
ui.pack(fill=tk.BOTH, expand=tk.YES)
root.mainloop()