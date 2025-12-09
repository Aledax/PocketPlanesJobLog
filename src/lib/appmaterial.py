from src.util.tkutil import *


FONT_FAMILY = 'Helvetica'

FONT_SIZE_LABEL = 10
FONT_SIZE_HEADER = 14

BG = 'lightblue'
BG_BUTTON = 'lightblue'
BG_BORDER_ROOT = '#4cb2c9'

PAD_HEADER = 10
PAD_BOX = 10
PAD_ENTRY_INSIDE = 4
BORDER_PANEL = 10
BORDER_ROOT = 15
BOX_WIDTH = 20
CELL_WIDTH = 4
LISTBOX_HEIGHT = 8
BUTTON_WIDTH = 10


class AppMaterial:

    def __init__(self, root: tk.Tk):

        self.root = root
        root.configure(bg=BG)
        root.configure(highlightthickness=BORDER_ROOT, highlightbackground=BG_BORDER_ROOT, highlightcolor=BG_BORDER_ROOT)
        self.register_validators(root)

    def register_validators(self, root: tk.Tk):

        self.validate_numeric_input = root.register(lambda P: P == '' or P.isdigit())
    
    def frame(self, master: tk.Widget, grid_kwargs: dict) -> tk.Frame:

        frame = tk.Frame(
            master,
            bg=BG,
        )
        frame.grid(
            **grid_kwargs
        )
        return frame

    def panel(self, master: tk.Widget, grid_kwargs: dict) -> tk.Frame:

        panel = tk.Frame(
            master,
            bg=BG,
            relief=tk.FLAT,
            borderwidth=BORDER_PANEL,
        )
        panel.grid(
            **grid_kwargs
        )
        return panel
    
    def spacer_v(self, master: tk.Widget, grid_kwargs: dict, height: int) -> tk.Frame:
        
        spacer = tk.Frame(
            master,
            height=height,
            bg=BG,
        )
        spacer.grid(
            **grid_kwargs
        )
        return spacer
    
    def spacer_h(self, master: tk.Widget, grid_kwargs: dict, width: int) -> tk.Frame:
        
        spacer = tk.Frame(
            master,
            width=width,
            bg=BG,
        )
        spacer.grid(
            **grid_kwargs
        )
        return spacer

    def header(self, master: tk.Widget, grid_kwargs: dict, text: str) -> tk.Label:
        
        header = tk.Label(
            master,
            text=text,
            font=(FONT_FAMILY, FONT_SIZE_HEADER, 'bold'),
            bg=BG,
        )
        header.grid(
            **grid_kwargs
        )
        return header
    
    def separator_h(self, master: tk.Widget, grid_kwargs: dict) -> ttk.Separator:
        
        separator = ttk.Separator(
            master,
            orient='horizontal',
        )
        separator.grid(
            padx=10,
            pady=10,
            sticky=tk.EW,
            **grid_kwargs
        )
        return separator
    
    def separator_v(self, master: tk.Widget, grid_kwargs: dict) -> ttk.Separator:
        
        separator = ttk.Separator(
            master,
            orient='vertical',
        )
        separator.grid(
            padx=10,
            pady=10,
            sticky=tk.NS,
            **grid_kwargs
        )
        return separator

    def label(self, master: tk.Widget, grid_kwargs: dict, text: str) -> tk.Label:
        
        label = tk.Label(
            master,
            text=text,
            font=(FONT_FAMILY, FONT_SIZE_LABEL, 'bold'),
            bg=BG,
        )
        label.grid(
            **grid_kwargs
        )
        return label
    
    def entry(self, master: tk.Widget, grid_kwargs: dict, numeric: bool=False, disabled: bool=False, width: int=BOX_WIDTH, type_command: callable=None, return_command: callable=None) -> tk.Entry:
        
        entry = tk.Entry(
            master,
            justify='center',
            font=(FONT_FAMILY, FONT_SIZE_LABEL),
            width=width,
            validate='key',
            validatecommand=(self.validate_numeric_input, '%P') if numeric else None
        )
        entry.grid(
            padx=PAD_BOX,
            pady=PAD_BOX,
            ipady=PAD_ENTRY_INSIDE,
            **grid_kwargs
        )
        if disabled:
            entry.configure(state='disabled')
        if type_command is not None:
            entry.bind('<KeyRelease>', lambda _: type_command())
        if return_command is not None:
            entry.bind('<Return>', lambda _: return_command())
        return entry
    
    def button(self, master: tk.Widget, grid_kwargs: dict, text: str, command: callable) -> tk.Button:
        
        button = tk.Button(
            master,
            text=text,
            font=(FONT_FAMILY, FONT_SIZE_LABEL, 'bold'),
            width=BUTTON_WIDTH,
            command=command,
            bg=BG_BUTTON,
        )
        button.grid(
            padx=PAD_BOX,
            pady=PAD_BOX,
            **grid_kwargs
        )
        return button
    
    def listbox(self, master: tk.Widget, grid_kwargs: dict, items: list, select_command: callable=None, return_command: callable=None) -> tk.Listbox:
        
        listbox = tk.Listbox(
            master,
            justify='center',
            font=(FONT_FAMILY, FONT_SIZE_LABEL),
            width=BOX_WIDTH,
            height=LISTBOX_HEIGHT,
            selectmode=tk.EXTENDED,
            activestyle='none'
        )
        listbox.grid(
            padx=PAD_BOX,
            pady=PAD_BOX,
            **grid_kwargs
        )
        for item in items:
            listbox.insert(tk.END, item)
        if select_command is not None:
            listbox.bind('<<ListboxSelect>>', lambda _: select_command())
        if return_command is not None:
            listbox.bind('<Return>', lambda _: return_command())
        return listbox