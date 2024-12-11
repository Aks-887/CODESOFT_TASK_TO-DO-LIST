from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

def add_task():  
    task_string = task_field.get()  
    if len(task_string) == 0:  
        messagebox.showinfo('Error', 'Field is Empty.')  
    else:    
        tasks.append(task_string)   
        the_cursor.execute('insert into tasks values (?)', (task_string ,))    
        list_update()    
        task_field.delete(0, 'end')  
    
def list_update():    
    clear_list()    
    for task in tasks:    
        task_listbox.insert('end', task)  
  
def delete_task():  
    try:  
        the_value = task_listbox.get(task_listbox.curselection())    
        if the_value in tasks:  
            tasks.remove(the_value)    
            list_update()   
            the_cursor.execute('delete from tasks where title = ?', (the_value,))  
    except:   
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')        
  
def delete_all_tasks():  
    message_box = messagebox.askyesno('Delete All', 'Are you sure?')  
    if message_box == True:    
        while(len(tasks) != 0):    
            tasks.pop()    
        the_cursor.execute('delete from tasks')   
        list_update()  
   
def clear_list():   
    task_listbox.delete(0, 'end')  
  
def close():    
    print(tasks)   
    guiWindow.destroy()  
    
def retrieve_database():    
    while(len(tasks) != 0):    
        tasks.pop()    
    for row in the_cursor.execute('select title from tasks'):    
        tasks.append(row[0])  
   
if __name__ == "__main__":   
    guiWindow = Tk()   
    guiWindow.title("To-Do List")  
    guiWindow.geometry("750x450+500+200")  # Updated dimensions
    guiWindow.resizable(0, 0)  
    guiWindow.configure(bg="#FFE4B5")  # Changed background color
   
    the_connection = sql.connect('listOfTasks.db')   
    the_cursor = the_connection.cursor()   
    the_cursor.execute('create table if not exists tasks (title text)')  
    
    tasks = []  
        
    functions_frame = Frame(guiWindow, bg="#F5DEB3")  # Changed frame color
    functions_frame.pack(side="top", expand=True, fill="both")  
  
    task_label = Label(
        functions_frame,
        text="TO-DO-LIST \n Enter the Task Title:",  
        font=("Arial", 14, "bold"),  
        background="#F5DEB3",  # Changed label background color
        foreground="#8B4513"  # Changed text color
    )    
    task_label.place(x=20, y=30)  
        
    task_field = Entry(  
        functions_frame,  
        font=("Arial", 14),  
        width=50,  
        foreground="black",
        background="white",  
    )    
    task_field.place(x=220, y=30)  
    
    add_button = Button(  
        functions_frame,  
        text="Add",  
        width=15,
        bg='#FFA07A', font=("Arial", 12, "bold"),  # Changed button colors
        command=add_task,
    )  
    del_button = Button(  
        functions_frame,  
        text="Remove",  
        width=15,
        bg='#FFA07A', font=("Arial", 12, "bold"),  
        command=delete_task,  
    )  
    del_all_button = Button(  
        functions_frame,  
        text="Delete All",  
        width=15,
        font=("Arial", 12, "bold"),
        bg='#FFA07A',
        command=delete_all_tasks  
    )
    
    exit_button = Button(  
        functions_frame,  
        text="Exit / Close",  
        width=62,
        bg='#FFA07A', font=("Arial", 12, "bold"),
        command=close  
    )    
    add_button.place(x=20, y=80)  
    del_button.place(x=260, y=80)  
    del_all_button.place(x=500, y=80)  
    exit_button.place(x=20, y=370)  
    
    task_listbox = Listbox(  
        functions_frame,  
        width=80,  
        height=10,  
        font=("Arial", 12),
        selectmode='SINGLE',  
        background="white",
        foreground="black",    
        selectbackground="#FFD700",  
        selectforeground="black"
    )    
    task_listbox.place(x=20, y=140)  
    
    retrieve_database()  
    list_update()    
    guiWindow.mainloop()    
    the_connection.commit()  
    the_cursor.close()
