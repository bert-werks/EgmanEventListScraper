import tkinter as tk
from tkinter import ttk
import pandas as pd
import ListGetter as lg

def do_it_all(url, root):
    links = lg.get_deckList_data(url)
    lists = lg.update_card_names(links)
    dataframes = lg.create_dataframes(lists)
    display_dataframes(root, dataframes)

def display_dataframes(root, dataframes):
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    for df in dataframes:
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=df.title)

        # Create a label to display the title
        title_label = ttk.Label(tab, text=df.title, font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=len(df.columns), pady=10, padx=10)

        # Create a DataFrame widget to display the DataFrame
        df_widget = ttk.Treeview(tab)
        df_widget['columns'] = df.columns.tolist()
        df_widget.heading('#0', text='')
        for col in df.columns:
            df_widget.heading(col, text=col)
            df_widget.column(col, width=100, anchor='center')
        for i, row in df.iterrows():
            df_widget.insert('', 'end', text=i, values=row.tolist())

        df_widget.grid(row=1, column=0, columnspan=len(df.columns), padx=10, pady=10)

def main():
    root = tk.Tk()
    root.title('Deck Analyzer')

    # Create a label to prompt the user for a URL
    url_label = ttk.Label(root, text='Enter a URL:')
    url_label.pack(pady=10)

    # Create an entry field to input the URL
    url_entry = ttk.Entry(root)
    url_entry.pack(pady=5)

    # Create a button to call do_it_all when pressed
    button = ttk.Button(root, text='Analyze', command=lambda: do_it_all(url_entry.get(), root))
    button.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()