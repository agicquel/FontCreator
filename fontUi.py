import tkinter as tk
import string


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
        self.charFrame = tk.Frame(self, relief=tk.GROOVE)
        self.charFrame.pack_propagate(0)
        self.charFrame.pack(side=tk.LEFT, anchor="n", fill=tk.BOTH, expand=tk.YES)
        self.ledsGrid = LedCanvas(self.charFrame, leds, self.on_led_clicked)
        self.ledsGrid.pack(fill=tk.BOTH, expand=tk.YES, padx=2, pady=2)

        self.controlFrame = tk.Frame(self, relief=tk.GROOVE, width=50, bg="white")
        self.controlFrame.pack(fill=tk.BOTH, expand=tk.YES, side=tk.RIGHT, anchor="n", padx=2, pady=2)
        scrollbar = tk.Scrollbar(self.controlFrame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.letters = {}
        self.lettersListBox = tk.Listbox(self.controlFrame, height=200)
        self.lettersListBox.config(yscrollcommand=scrollbar.set)
        self.lettersListBox.pack(fill=tk.X)
        scrollbar.config(command=self.lettersListBox.yview)

        for letter in list(string.ascii_uppercase):
            self.addLetter(letter, list())
        self.lettersListBox.select_set(0)
        self.selectedLetter = 0
        self.lettersListBox.bind('<<ListboxSelect>>', self.on_letterlist_select)

        self.buttonsFrame = tk.Frame(self, relief=tk.GROOVE, width=50, bg="white")
        self.buttonsFrame.pack(fill=tk.BOTH, expand=tk.YES, side=tk.RIGHT, anchor="s", padx=2, pady=2)
        generateButton = tk.Button(self.buttonsFrame, height=30, width=30, text="Générer", command=self.generate_font)
        generateButton.pack(side=tk.BOTTOM)

    def addLetter(self, letter, leds):
        self.letters[len(self.letters)] = (letter, leds)
        self.lettersListBox.insert(len(self.letters), letter + " : " + str(leds))

    def on_letterlist_select(self, event):
        index = int(event.widget.curselection()[0])
        if index == self.selectedLetter:
            return
        self.letters[self.selectedLetter] = (self.letters[self.selectedLetter][0], self.ledsGrid.exportSelected())

        self.lettersListBox.delete(self.selectedLetter)
        self.lettersListBox.insert(self.selectedLetter, self.letters[self.selectedLetter][0] + " : " + str(
            self.letters[self.selectedLetter][1]))

        self.selectedLetter = index
        self.ledsGrid.reset()
        self.ledsGrid.importSelected(self.letters[self.selectedLetter][1])

    def on_led_clicked(self, led_id, led_selected):
        self.lettersListBox.delete(self.selectedLetter)
        self.lettersListBox.insert(self.selectedLetter, self.letters[self.selectedLetter][0] + " : " + str(led_selected))

    def generate_font(self):
        print("bouton")
