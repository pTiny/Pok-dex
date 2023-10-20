import tkinter as tk
from tkinter import *
from PIL import  ImageTk, Image
import requests as rq

# fetching pokemon information from Pokemon API
poke_number = 150 # number of pokemon in the pokedex we want
pokemon_names = [] # list of the names of pokemon we fetch
pokemon_objs = [] # list of pokemon as instances of the Pokemon() class

response = rq.get(f"https://pokeapi.co/api/v2/pokemon?limit={poke_number}") # fetching data on each pokemon from API
for i in response.json()['results']:
    pokemon_names.append(i['name']) # adds name of each pokemon in response to the list of pokemon names that will be in the pokedex


# defining class each pokemon object will belong to
class Pokemon:
    def __init__(self, name): # types, dex_entries
        self.name = name
        self.sprite_location = "LOCATION_OF_SPRITE_IN_DIRECTORY" # replace contents of this string with the location of sprite in directory
        self.json_file = rq.get(f"https://pokeapi.co/api/v2/pokemon/{self.name}")
        self.stats = f'''
HP: {self.json_file.json()['stats'][0]['base_stat']}
Attack: {self.json_file.json()['stats'][1]['base_stat']}
Defense: {self.json_file.json()['stats'][2]['base_stat']}
Special Attack: {self.json_file.json()['stats'][3]['base_stat']}
Special Defense: {self.json_file.json()['stats'][4]['base_stat']}
Speed: {self.json_file.json()['stats'][5]['base_stat']}
Total: {self.json_file.json()['stats'][0]['base_stat'] + self.json_file.json()['stats'][1]['base_stat'] + self.json_file.json()['stats'][2]['base_stat'] + self.json_file.json()['stats'][3]['base_stat'] + self.json_file.json()['stats'][4]['base_stat'] + self.json_file.json()['stats'][5]['base_stat']}
            '''
        
    def types(self): # function that returns the type(s) of given pokemon
        try:
            type_2 = self.json_file.json()['types'][1]['type']['name']
        except:
            type_2 = ''
        types = self.json_file.json()['types'][0]['type']['name'].capitalize() + ' ' + type_2.capitalize()
        return types
    
    def dex_entries(self): # function that returns the pokedex entries of given pokemon
        dexentries = {}
        species = rq.get(self.json_file.json()['species']['url'])
        for i in species.json()['flavor_text_entries']:
            if i['language']['name'] == 'en':
                dexentries[i['version']['name']] = i['flavor_text']
            else:
                pass
        for i in dexentries:
            i = f"{i.capitalize()}: {dexentries[i]}"
        return dexentries

for pokemon in pokemon_names:
    pokemon_objs.append(Pokemon(pokemon)) # adds each pokemon as an instance of the Pokemon() class to a list of objects


# defining class window object will belong to
class MainWindow(Tk):
    def __init__(self, title, geometry):
        # initialization
        super().__init__()
        self.title(title) # string setting title of the window
        self.geometry(f'{geometry[0]}x{geometry[1]}') # string of form 'width x height' setting the geometry of the window
        self.minsize(geometry[0],geometry[1]) # setting minimum size of window
        
        # main scrollable background
        self.main_pokedex = MainPokedex(self)

        # run
        self.mainloop()


class MainPokedex(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.scroll_frame() # on initialization, it makes the frame scrollable

    
    def restore_frame(self, root): # function that restores a frame to the original state (the main menu)
        for widget in root.winfo_children():
            widget.destroy()

        self.main_page_widgets(root)

    def clear_frame(self, root, pokemon): # function that clears all widgets in a frame and displays information on individual pokemon, back button takes user back to main screen
        for widget in root.winfo_children():
            widget.destroy()

        self.secondary_page_widgets(root, pokemon)

    def main_page_widgets(self, root):
        # pokemon logo at top of main page
        logo_image = ImageTk.PhotoImage(Image.open("LOCATION_OF_POKEMON_LOGO_IN_DIRECTORY").resize((200,68))) # replace contents of this string with the location of pokemon logo in directory
        logo_image_label = tk.Label(root, image=logo_image, background='black') # , background='black'
        logo_image_label.image = logo_image
        logo_image_label.grid(row=1 ,column=2, rowspan=2, columnspan=4)
        
        # assigns each pokemon a button & adds it and its sprite to the main window of the application in 6 column grid format
        x,y=0,1
        for i in pokemon_objs:
            if pokemon_objs.index(i)%6 == 0:
                y=y+2
                x=0
            x=x+1
            sprite_image = ImageTk.PhotoImage(Image.open(i.sprite_location))
            image_label = tk.Label(root, image=sprite_image, background='black')
            image_label.image = sprite_image
            image_label.grid(row=y ,column=x, columnspan=1) # int(pokemon_objs.index(i))
            button = Button(root, text=i.name.capitalize(), command=lambda i=i: self.clear_frame(root, i))
            button.grid(row=y+1 ,column=x, columnspan=1)
        
        
    def secondary_page_widgets(self, root, pokemn):
        # widgets for the secondary page
        name_label = tk.Label(root, text=pokemn.name.capitalize(), background='black', foreground='white')
        name_label.grid(row=1 ,column=1, columnspan=6)
        sprite_image = ImageTk.PhotoImage(Image.open(pokemn.sprite_location).resize((200,200)))
        image_label = tk.Label(root, image=sprite_image, background='black')
        image_label.image = sprite_image
        image_label.grid(row=2 ,column=3, columnspan=2, rowspan=2)
        types_label = tk.Label(root, text=pokemn.types(), background='black', foreground='white')
        types_label.grid(row=5 ,column=1, columnspan=6)
        stats_label = tk.Label(root, text=pokemn.stats, background='black', foreground='white')
        stats_label.grid(row=6 ,column=1, columnspan=6)

        a=7
        for i in pokemn.dex_entries():
            dex_entries_label = tk.Label(root, text=f'{i.capitalize()}: {pokemn.dex_entries()[i].capitalize()}', background='black', foreground='white')
            dex_entries_label.grid(row=a ,column=1, columnspan=6, pady=20)
            a=a+1

        back_bttn = Button(root, text=f'Back', command=lambda: self.restore_frame(root))
        back_bttn.grid(row=a ,column=1, columnspan=6)


    # main resusable frame
    def scroll_frame(self):
        def FrameWidth(event):
            main_canvas.itemconfig(main_canvas_window_frame, width=event.width)

        def OnFrameConfigure(event):
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))

        # creating main canvas (which can be scrolled)
        main_canvas = Canvas(self, background='green')
        main_canvas.pack(fill='both', expand=True, side='left') # pack(fill=BOTH, expand=1, side=LEFT)

        # creating usable subframe within main canvas (this is where all of the main components of every page will be)
        sub_frame = Frame(main_canvas, bg='black')

        # adding subframe to a window within the canvas
        main_canvas_window_frame = main_canvas.create_window((0,0), window=sub_frame, anchor='nw')

        # adding scrollbar to canvas in main frame
        scrollbar = Scrollbar(self, orient='vertical', command=main_canvas.yview) # scroll bar
        scrollbar.pack(side='right', fill='y') # putting scroll bar to far right of the window

        # configuring scrollbar to work on canvas
        main_canvas.config(yscrollcommand=scrollbar.set)
        
        sub_frame.bind('<Configure>', OnFrameConfigure)
        main_canvas.bind('<Configure>', FrameWidth)
        
        # configuring the grid of the sub_frame
        sub_frame.columnconfigure((0,1,2,3,4,5,6,7), weight=1)

        self.main_page_widgets(sub_frame)


MainWindow('Kanto Pokédex', (627,500))
print("Render complete.")