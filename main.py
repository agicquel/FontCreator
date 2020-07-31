from netlistParser import *
from fontUi import *
import pyinstaller_path

pcb = PcbParse(pyinstaller_path.resource_path("./pcb/pcb.kicad_pcb"))
leds = pcb.analyse_leds()

root = tk.Tk()
root.title("Pasteur Font Creator")
root.geometry("900x800")
ui = FontUI(root, leds)
ui.pack(fill=tk.BOTH, expand=tk.YES)
root.mainloop()
