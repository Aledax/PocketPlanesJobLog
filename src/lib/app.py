from src.lib.appmaterial import *
from src.lib.datainterface import *


TITLE = 'Pocket Planes Job Logger'


class TkApp(tk.Tk):

    def __init__(self):

        super().__init__()
        self.title(TITLE)
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)

        self.cities_data = data_load_cities()
        self.selected_cities = []

        self.material = AppMaterial(self)
        self.initialize_layout()

    def initialize_layout(self):

        self.create_city_panel = self.material.panel(self, {'row': 0, 'column': 0})
        self.create_city_header = self.material.header(
            self.create_city_panel,
            {'row': 0, 'column': 0, 'columnspan': 2},
            'Create City'
        )
        self.create_city_header_spacer = self.material.spacer_v(
            self.create_city_panel,
            {'row': 1, 'column': 0, 'columnspan': 2},
            PAD_HEADER
        )
        self.create_city_name_label = self.material.label(
            self.create_city_panel,
            {'row': 2, 'column': 0},
            'Name'
        )
        self.create_city_name_entry = self.material.entry(
            self.create_city_panel,
            {'row': 3, 'column': 0},
            type_command=self.update_create_city_button,
            return_command=self.create_city
        )
        self.create_city_population_label = self.material.label(
            self.create_city_panel,
            {'row': 4, 'column': 0},
            'Pop. (100K)'
        )
        self.create_city_population_entry = self.material.entry(
            self.create_city_panel,
            {'row': 5, 'column': 0},
            numeric=True,
            type_command=self.update_create_city_button,
            return_command=self.create_city
        )
        self.create_city_button = self.material.button(
            self.create_city_panel,
            {'row': 2, 'column': 1, 'rowspan': 4, 'sticky': tk.NS},
            'Create\nCity',
            self.create_city
        )
        self.update_create_city_button()

        self.create_city_separator = self.material.separator_h(self, {'row': 1, 'column': 0})

        self.select_city_panel = self.material.panel(self, {'row': 2, 'column': 0})
        self.select_city_header = self.material.header(
            self.select_city_panel,
            {'row': 0, 'column': 0, 'columnspan': 2},
            'Select Cities'
        )
        self.select_city_header_spacer = self.material.spacer_v(
            self.select_city_panel,
            {'row': 1, 'column': 0, 'columnspan': 2},
            PAD_HEADER
        )
        self.select_city_listbox = self.material.listbox(
            self.select_city_panel,
            {'row': 2, 'column': 0},
            [],
            select_command=self.update_select_city_button,
            return_command=self.update_record_matrix
        )
        self.select_city_button = self.material.button(
            self.select_city_panel,
            {'row': 2, 'column': 1, 'sticky': tk.NS},
            'Generate\nRecord\nTable',
            self.update_record_matrix
        )
        self.update_select_city_listbox()
        self.update_select_city_button()

        self.config_separator = self.material.separator_v(self, {'row': 0, 'column': 1, 'rowspan': 3})

        self.record_panel = self.material.panel(self, {'row': 0, 'column': 2, 'rowspan': 3, 'sticky': tk.N})
        self.record_header = self.material.header(
            self.record_panel,
            {'row': 0, 'column': 0},
            'Job Counts'
        )
        self.record_header_spacer = self.material.spacer_v(
            self.record_panel,
            {'row': 1, 'column': 0},
            PAD_HEADER
        )
        self.record_gridframe = self.material.frame(
            self.record_panel,
            {'row': 2, 'column': 0}
        )
        self.record_gridframe_cells = {}
        self.first_gridframe_cell = None
        self.record_create_button = self.material.button(
            self.record_panel,
            {'row': 3, 'column': 0, 'sticky': tk.EW},
            'Add Record',
            self.create_record
        )
        self.update_record_matrix()
        self.update_create_record_button()

    def record_matrix_has_data(self) -> bool:

        for row_cells in self.record_gridframe_cells.values():
            for cell in row_cells.values():
                if cell.get().strip() != '':
                    return True
        return False

    def create_city(self):

        name = self.create_city_name_entry.get()
        population_100k = self.create_city_population_entry.get()

        result = data_create_city(name, population_100k)
        if not result:
            tk.messagebox.showerror(
                TITLE,
                'City already exists or invalid input!'
            )
            return
        
        self.create_city_name_entry.delete(0, tk.END)
        self.create_city_population_entry.delete(0, tk.END)
        self.create_city_name_entry.focus_set()
        self.update_select_city_listbox()

    def create_record(self):

        if not self.record_matrix_has_data():
            tk.messagebox.showerror(
                TITLE,
                'No data to create record!'
            )
            return

        counts = {
            row_city: {
                col_city: int(self.record_gridframe_cells[row_city][col_city].get() or 0)
                for col_city in self.selected_cities
            } for row_city in self.selected_cities
        }

        result = data_create_record(self.selected_cities, counts)
        if not result:
            tk.messagebox.showerror(
                TITLE,
                'Failed to create record!'
            )
            return

        for row_cells in self.record_gridframe_cells.values():
            for cell in row_cells.values():
                cell.delete(0, tk.END)
        if self.first_gridframe_cell:
            self.first_gridframe_cell.focus_set()
        self.update_create_record_button()

    def update_create_city_button(self):

        name = self.create_city_name_entry.get().strip()
        population_100k = self.create_city_population_entry.get().strip()
        is_valid = name != '' and population_100k != '' and population_100k.isdigit()
        self.create_city_button.configure(state='normal' if is_valid else 'disabled')

    def update_select_city_listbox(self):

        self.cities_data = data_load_cities()
        city_names = [city['name'].title() for city in self.cities_data]
        self.select_city_listbox.delete(0, tk.END)
        for name in city_names:
            self.select_city_listbox.insert(tk.END, name)

    def update_select_city_button(self):

        selected_indices = self.select_city_listbox.curselection()
        selected_cities = [self.cities_data[i]['name'] for i in selected_indices]
        self.select_city_button.configure(state='normal' if len(selected_cities) >= 2 else 'disabled')

    def update_record_matrix(self):

        previous_cell_values = {
            row_city: {col_city: cell.get() for col_city, cell in row_cells.items()}
            for row_city, row_cells in self.record_gridframe_cells.items()
        }

        selected_indices = self.select_city_listbox.curselection()
        self.selected_cities = [self.cities_data[i]['name'] for i in selected_indices]
        self.record_create_button.configure(state='normal' if len(self.selected_cities) >= 2 else 'disabled')

        self.record_gridframe_cells = {}
        self.first_gridframe_cell = None
        for widget in self.record_gridframe.winfo_children():
            widget.destroy()

        for row, row_city in enumerate(self.selected_cities):

            self.material.label(
                self.record_gridframe,
                {'row': 0, 'column': row + 1},
                row_city.capitalize()
            )
            self.material.label(
                self.record_gridframe,
                {'row': row + 1, 'column': 0},
                row_city.capitalize()
            )
            row_cells = {}

            for col, col_city in enumerate(self.selected_cities):
                row_cells[col_city] = self.material.entry(
                    self.record_gridframe,
                    {'row': row + 1, 'column': col + 1},
                    numeric=True,
                    disabled=(row == col),
                    width=CELL_WIDTH,
                    type_command=self.update_create_record_button,
                    return_command=self.create_record
                )
                if row_city in previous_cell_values and col_city in previous_cell_values[row_city]:
                    row_cells[col_city].insert(0, previous_cell_values[row_city][col_city])
                if row == 0 and col == 1:
                    self.first_gridframe_cell = row_cells[col_city]

            self.record_gridframe_cells[row_city] = row_cells

        self.select_city_listbox.selection_clear(0, tk.END)
        self.update_select_city_button()
        if self.first_gridframe_cell:
            self.first_gridframe_cell.focus_set()
        self.update_create_record_button()

    def update_create_record_button(self):

        self.record_create_button.configure(state='normal' if self.record_matrix_has_data() else 'disabled')


if __name__ == '__main__':

    app = TkApp()
    app.mainloop()