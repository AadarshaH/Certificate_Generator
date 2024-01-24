import os
import cv2
import tkinter as tk
from tkinter import font as tkfont

list_of_names = []


#delete the old certificates when the program is run again
def delete_old_data():
    for i in os.listdir(r"generated-certificates"):
        os.remove("generated-certificates/{}".format(i))


#cleanup the data in the notepad so that there are no excess spaces
def cleanup_data():
    with open(r'Extras\name_students_data_temp.txt') as data:
        for line in data:
            name, score = line.split(':')
            list_of_names.append((name.strip(), score.strip()))

#function to generate the certificates
def generate_certificates():
    for index, (name, score) in enumerate(list_of_names):
        certificate_template_image = cv2.imread("images\Certificate-template.jpg")
        cv2.putText(certificate_template_image, name, (248, 291), cv2.FONT_ITALIC, 1, (0, 0, 0), 4, cv2.LINE_AA)
        cv2.putText(certificate_template_image, score, (364, 383), cv2.FONT_ITALIC, 1, (0, 0, 0), 4, cv2.LINE_AA)
        cv2.imwrite("generated-certificates/{}.jpg".format(name), certificate_template_image)
        print("Processing {} / {}".format(index + 1,len(list_of_names)))

#save the data obtained from the form to a text file
def save_to_file(name, percentage):
    with open('Extras\\name_students_data_temp.txt', 'a') as data:
        data.write(f'{name}: {percentage}\n')

    with open('Database\\name_students_data.txt', 'a') as data:
        data.write(f'{name}: {percentage}\n')


#haruna's part starts(
#setting the action when the submit button is clicked
def submit_form(entries, root):
    name = entries['Name'].get()
    subjects = ['Math', 'Science', 'English', 'History', 'Geography']
    total_score = 0
    for subject in subjects:
        score = float(entries[subject].get())
        total_score += score
    percentage = (total_score / (len(subjects) * 100)) * 100
    save_to_file(name, percentage)
    delete_old_data()
    cleanup_data()
    generate_certificates()
    open('Extras\\name_students_data_temp.txt', 'w').close()  # Clear the text file after generating certificates
    root.quit()


#creating the form
def make_form(root, fields):
    root.title("Data Entry")
    root.geometry("500x300")  # Set the window size
    root.configure(bg='light blue')
    entries = {}
    my_font = tkfont.Font(family="Helvetica", size=14)
    for field in fields:
        row = tk.Frame(root, bg='light blue')
        lab = tk.Label(row, width=20, text=f"Enter the score in {field}" if field != 'Name' else "Enter your name", anchor='w', font=my_font, bg='light blue')
        ent = tk.Entry(row, font=my_font)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries[field] = ent
    return entries
#)haruna's part ends

if __name__ == '__main__':
    subjects = ['Name', 'Math', 'Science', 'English', 'History', 'Geography']
    root = tk.Tk()
    root.configure(bg='light blue')
    ents = make_form(root, subjects)
    root.bind('<Return>', (lambda event, e=ents: submit_form(e, root)))   
    b1 = tk.Button(root, text='Submit', command=(lambda e=ents: submit_form(e, root)), font=("Helvetica", 16), bg='light green')
    b1.pack(side=tk.BOTTOM, padx=5, pady=5)
    root.mainloop()

