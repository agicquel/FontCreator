import tkinter as tk
import string
from font_generator import FontGenerator


class LedCanvas(tk.Canvas):
    def __init__(self, parent, leds, ledSelectedCallback=None, **kwargs):
        tk.Canvas.__init__(self, parent, bg="white", **kwargs)
        self.leds = leds
        self.ledSelectedCallback = ledSelectedCallback
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        maxCol = list(map(max, zip(*self.leds)))
        (self.max_x, self.max_y) = (maxCol[1], maxCol[2])
        self.rect = {}
        self.drawLeds()
        self.selected = []

    def drawLeds(self):
        led_height = 12
        led_width = 16

        m = 0.95 * min((self.height / self.max_y), (self.width / self.max_x))
        for led in self.leds:
            x = led[1] * m
            y = led[2] * m

            if (led[3] / 90) % 2 == 0:
                (x1, y1, x2, y2) = (x - (led_width / 2), y - (led_height / 2), x + (led_width / 2),
                                    y + (led_height / 2))
            else:
                (x1, y1, x2, y2) = (x - (led_height / 2), y - (led_width / 2), x + (led_height / 2),
                                    y + (led_width / 2))
            if led[0] not in self.rect:
                self.rect[led[0]] = self.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                self.tag_bind(self.rect[led[0]], "<Button-1>", self.rect_clicked)
            else:
                self.coords(led[0], x1, y1, x2, y2)

        self.width = self.max_x * m
        self.config(width=self.width, height=self.height)
        self.update()

    def on_resize(self, event):
        # wscale = float(event.width)/self.width
        # hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        self.config(width=self.width, height=self.height)
        # resize the canvas
        # rescale all the objects tagged with the "all" tag
        # self.scale("all",0,0,wscale,hscale)
        self.drawLeds()

    def rect_clicked(self, event):
        rect = event.widget.find_withtag('current')[0]
        led_id = list(self.rect.keys())[list(self.rect.values()).index(rect)]
        if led_id not in self.selected:
            self.itemconfig(rect, fill="yellow")
            self.selected.append(led_id)
        else:
            self.itemconfig(rect, fill="white")
            self.selected.remove(led_id)
        if self.ledSelectedCallback is not None:
            self.ledSelectedCallback(led_id, self.selected)

    def reset(self):
        for r in self.rect.values():
            self.itemconfig(r, fill="white")
        self.selected = []

    def exportSelected(self):
        return self.selected

    def importSelected(self, selected):
        self.selected = selected
        for s in selected:
            rect = self.rect[s]
            self.itemconfig(rect, fill="yellow")


class FontUI(tk.Frame):
    def __init__(self, root, leds):
        tk.Frame.__init__(self, root)
        root.pack_propagate(0)

        # Frames
        charFrame = tk.Frame(self, relief=tk.GROOVE)
        #pcharFrame.pack_propagate(0)
        charFrame.pack(side=tk.LEFT, anchor="n", fill=tk.BOTH, expand=tk.YES)
        controlFrame = tk.Frame(self, relief=tk.GROOVE, width=50, bg="white")
        controlFrame.pack(fill=tk.BOTH, expand=tk.YES, side=tk.RIGHT, anchor="n", padx=2, pady=2)
        buttonsFrame = tk.Frame(controlFrame, bd=1, relief=tk.RAISED, bg="ivory")
        buttonsFrame.config(height=200)
        buttonsFrame.grid(row=0, column=0, sticky="NESW")
        buttonsFrame.grid_rowconfigure(0, weight=1)
        buttonsFrame.grid_columnconfigure(0, weight=1)
        buttonsFrame.pack(side=tk.BOTTOM, fill=tk.X, anchor="e", padx=2, pady=2)

        # Buttons
        #tk.Button(buttonsFrame, width=30, text='Ajouter une lettre').grid()
        tk.Button(buttonsFrame, width=30, text='Clear la lettre', command=self.reset_selected_letter).grid()
        tk.Button(buttonsFrame, width=30, text='Tout supprimer', command=self.reset_font).grid()
        tk.Button(buttonsFrame, width=30, text='Générer la font', command=self.generate_font).grid()

        # Led Grid
        self.ledsGrid = LedCanvas(charFrame, leds, self.on_led_clicked)
        self.ledsGrid.pack(fill=tk.BOTH, expand=tk.YES, padx=2, pady=2)

        # Letter list with scrollbar
        scrollbar = tk.Scrollbar(controlFrame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.letters = {}
        self.lettersListBox = tk.Listbox(controlFrame, height=200)
        self.lettersListBox.config(yscrollcommand=scrollbar.set)
        self.lettersListBox.bind('<<ListboxSelect>>', self.on_letterlist_select)
        self.lettersListBox.pack(fill=tk.X)
        scrollbar.config(command=self.lettersListBox.yview)

        # Import default latin alphabet in letter list
        self.selectedLetter = 0
        self.reset_font()


    def addLetter(self, letter, leds):
        self.letters[len(self.letters)] = (letter, leds)
        self.lettersListBox.insert(len(self.letters), letter + " : " + str(leds))

    def _update_selected_letter_list(self):
        self.lettersListBox.delete(self.selectedLetter)
        self.lettersListBox.insert(self.selectedLetter, self.letters[self.selectedLetter][0] + " : " + str(
            self.letters[self.selectedLetter][1]))

    def on_letterlist_select(self, event):
        index = int(event.widget.curselection()[0])
        if index == self.selectedLetter:
            return
        self.letters[self.selectedLetter] = (self.letters[self.selectedLetter][0], self.ledsGrid.exportSelected())
        self._update_selected_letter_list()
        self.selectedLetter = index
        self.ledsGrid.reset()
        self.ledsGrid.importSelected(self.letters[self.selectedLetter][1])

    def on_led_clicked(self, led_id, led_selected):
        self.letters[self.selectedLetter] = (self.letters[self.selectedLetter][0], self.ledsGrid.exportSelected())
        self._update_selected_letter_list()

    def reset_selected_letter(self):
        self.letters[self.selectedLetter] = (self.letters[self.selectedLetter][0], [])
        self._update_selected_letter_list()
        self.ledsGrid.reset()

    def reset_font(self):
        self.lettersListBox.delete(0, len(self.letters))
        self.letters.clear()
        for letter in list(string.ascii_uppercase):
            self.addLetter(letter, list())
        for number in range(10):
            self.addLetter(str(number), list())
        self.lettersListBox.select_set(0)
        self.selectedLetter = 0
        self.ledsGrid.reset()

    def generate_font(self):
        print("letters : \n" + str(self.letters))
        fg = FontGenerator(self.letters)
        fg.generateFontCode("./font.cpp")
        fg.generateFontHeader("./font.h")
