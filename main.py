from pydicom import dcmread
from pydicom.fileset import FileSet
from pydicom import Dataset
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

# Tkinter CRUD Methods:
def add():
    folder_selected = filedialog.askdirectory()
    folderPath.set(folder_selected)
    if folderPath.get() != "":
        image_data_path.append(folderPath.get())
        lb.insert('end', folderPath.get())


def remove():
    selected = lb.curselection()
    for selected_item in selected[::-1]:
        lb.delete(selected_item)
        image_data_path.pop(selected_item)


def select_save_path():
    folder_selected = filedialog.askdirectory()
    save_to_path.set(folder_selected)
    save_path_text_field.delete(1.0,END)
    save_path_text_field.insert(END,save_to_path.get())

def increment_progressbar():
    progressbar.step(1)
    style.configure('text.Horizontal.TProgressbar',
                    text='%i of %i Patients completed' % (0, len(image_data_path)))
    frame.after(200, increment_progressbar)


def generate_DICOMDIR():
    fs = FileSet()
    ds = Dataset()
    i = 0
    patient_iterator = 0
    try:
        if save_to_path.get() != "":
            generate_button.grid_remove()
            progressbar = ttk.Progressbar(frame, orient=HORIZONTAL, length=progress_bar_length, mode="indeterminate")
            progressbar.grid(column=0, row=18, columnspan=4, sticky=(W, E), padx=(0, 5))
            for patient in image_data_path:
                for instance in os.listdir(image_data_path[patient_iterator]):
                    ds = dcmread(f"{image_data_path[patient_iterator]}/{instance}")
                    ds.PatientID = str(patient_iterator)
                    ds.StudyID = str(i)
                    fs.add(ds)
                    i += 1
                    progressbar.step()
                    frame.update_idletasks()

                patient_iterator += 1

            fs.write(save_to_path.get())
            progressbar.grid_remove()
            generate_button.grid(column=0, row=18, padx=5, columnspan=4)

            frame.update_idletasks()
            messagebox.showinfo("Done", message="Generation Done..")
        else:
            messagebox.showerror("Error", message="Select a location to save the generated file..")
    except:
        progressbar.grid_forget()
        messagebox.showerror(title="Error", message="Something went wrong..")



# Build TkInter
root = Tk()
root.title("Generate DICOMDIR-File")
root.geometry("500x320")
root.resizable(False, False)
# Create Custom Progressbar-Styling
style = ttk.Style(root)
# Add Label in the Layout
style.layout('text.Horizontal.TProgressbar',
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar',
                              {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'}),
              ('Horizontal.Progressbar.label', {'sticky': 'nswe'})])
style.configure('text.Horizontal.TProgressbar', text='Hello Testing this shit', anchor='center')


# TkInter Variables
image_data_path = []
progress_bar_length = len(image_data_path)
save_to_path = StringVar()
folderPath = StringVar()
progressbar_increment_variable = DoubleVar()

# Create Frame and Grid Layout
frame = ttk.Frame(root, padding=(5,5,25,0), relief=SOLID)
frame.grid(column=0, row=0, sticky=(N,W,E,S))
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=1)

# Create Widgets
info_label = Label(frame, text="1. Select Folder(s) with DICOM Image Series:", anchor=NW)
lb = Listbox(frame, height=1, width=65, selectmode=MULTIPLE, selectborderwidth=2)
add_button = ttk.Button(frame, text="Add", command=add)
remove_button = ttk.Button(frame, text="Remove", command=remove)
save_label = Label(frame, text="2. Select the Save Location:", anchor=NW)
save_to_button = ttk.Button(frame, text="Select", command=select_save_path)
save_path_text_field = Text(frame, height=1, width=10)
progressbar = ttk.Progressbar(frame, orient=HORIZONTAL, length=progress_bar_length, style='text.Horizontal.TProgressbar')

generate_button = ttk.Button(frame, text="3. Generate", command=generate_DICOMDIR)
scroll_v = Scrollbar(lb)
scroll_h = Scrollbar(lb, orient=HORIZONTAL)

# Grid the Widgets
info_label.grid(column=0, row=0, sticky=(W,E))
lb.grid(column=0, row=1, sticky=(N,S,E,W), rowspan=14)
add_button.grid(column= 1, row= 1, sticky=(N,E), padx=5)
remove_button.grid(column=1, row=2, sticky=(N,E), padx=5)
# Add empty Rows in Column 2
for i in range(4, 10):
    Label(frame, text="").grid(column=1, row=i)
save_label.grid(column=0, row=15, sticky=(W,E),)
save_path_text_field.grid(column=0, sticky=(N,S,E,W))
save_to_button.grid(column=1, row=16, sticky=(N,E), padx=5)
Label(frame, text="").grid(column=1, row=17)
generate_button.grid(column=0, row=18, padx=5, columnspan=4)
Label(frame, text="").grid(column=1, row=19)
Label(frame, text="").grid(column=1, row=20)


root.mainloop()


