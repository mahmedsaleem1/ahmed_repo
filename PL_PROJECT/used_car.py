import tkinter
import joblib
import pandas as pd
from tkinter import *
from PIL import Image, ImageTk, ImageFilter
import sqlite3

file_path = 'Used_Car.joblib'
model = joblib.load(file_path)

conn = sqlite3.connect('used_car.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS login (
        username TEXT PRIMARY KEY,
        password varchar NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS register (
        username TEXT PRIMARY KEY,
        password varchar NOT NULL,
        phone INTEGER NOT NULL,
        email varchar NOT NULL,
        full_name TEXT NOT NULL
    )
''')
logged_in = False
# ******************************FUNCTIONS*******************************
def register_db_manage():
    new_uname = uname_reg_e.get()
    new_fname = fname_reg_e.get()
    new_pass = pass_reg_e.get()
    new_phn = phn_reg_e.get()
    new_email = email_reg_e.get()

    try:
        cursor.execute('''SELECT username FROM register''')
        uname_check = cursor.fetchall()
        usernames = [username[0] for username in uname_check]
        if (new_uname not in usernames):
            cursor.execute('''INSERT INTO register (username, full_name, password, phone, email)
                                VALUES (?, ?, ?, ?, ?)
                                ''', (new_uname, new_fname, new_pass, new_phn, new_email))
            cursor.execute('''INSERT INTO login (username, password)
                                VALUES (?, ?)
                                ''', (new_uname, new_pass))
            availablity_reg_check.config(text="Registered Successfully\nLogin to continue")
        elif(new_uname in usernames):
            availablity_reg_check.config(text="Kindly chose a different username\nSomeone with this username already exists")

        uname_reg_e.delete(0, 'end')
        fname_reg_e.delete(0, 'end')
        pass_reg_e.delete(0, 'end')
        phn_reg_e.delete(0, 'end')
        email_reg_e.delete(0, 'end')

        conn.commit()

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

def login_db_manage():
    uname_enter = uname_e.get()
    passw_enter = pass_e.get()
    try:
        cursor.execute('''SELECT username FROM login''')
        uname_check = cursor.fetchall()
        cursor.execute('''SELECT password FROM login''')
        pass_check = cursor.fetchall()

        usernames = [username[0] for username in uname_check]
        passwords = [password[0] for password in pass_check]

        if (uname_enter in usernames) and (passw_enter in passwords):
            show_succeed_login()
            global logged_in
            logged_in=True
        elif (len(uname_enter)==0 or len(passw_enter)==0):
            availablity_check.config(text='Fields cannot be empty!')
        elif (uname_enter not in usernames) and (passw_enter in passwords):
            availablity_check.config(text='Incorrect UserName')
        elif (uname_enter in usernames) and (passw_enter not in passwords):
            availablity_check.config(text='Incorrect Password')
        elif (uname_enter not in usernames) and (passw_enter not in passwords):
            availablity_check.config(text='Please Register First')
        else:
            availablity_check.config(text='Something went wrong')

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    conn.commit()

def model_pred():
    try:
        brand_value = brand_e.get()
        fuel_value = fuel_e.get()
        kms_value = int(km_d_e.get())
        model_value = car_model_e.get()
        city_value = reg_city_e.get()
        year_value = int(year_e.get())

        input_data = pd.DataFrame([[brand_value, fuel_value, kms_value, model_value, city_value, year_value]],
                                   columns=['Brand', 'Fuel', 'KMs Driven', 'Model', 'Registered City', 'Year'])

        predictions = model.predict(input_data)
        predict_val_l.config(text=f"THE PREDICTED PRICE IS: {int(predictions[0])} Rs/-")
    except ValueError:
        predict_val_l.config(text=f"Please Fill Valid Entries")
    except Exception:
        predict_val_l.config(text=f"The Model is out of Order")
def display_image():
    image_path = "car.png"
    image_label.image = ImageTk.PhotoImage(Image.open(image_path))
    image_label.config(image=image_label.image)
    image_label.place(x=240,y=0)

def log_image():
    image_path = "log_car.png"
    log_image_label.image = ImageTk.PhotoImage(Image.open(image_path))
    log_image_label.config(image=log_image_label.image)
    log_image_label.place(x=450,y=225)

def copy_right_img():
    image_path = "dazzle.png"
    copyright_image.image = ImageTk.PhotoImage(Image.open(image_path))
    copyright_image.config(image=copyright_image.image)
    copyright_image.place(x=220,y=393)

def login_stat():
    if logged_in==True:
        login_status.config(text="LOGIN STATUS : ACTIVE")
    elif logged_in==False:
        login_status.config(text="LOGIN STATUS : NOT ACTIVE")

def show_home():
    register_form.place_forget()
    prediction.place_forget()
    registration.place_forget()
    home.place(x=0,y=0)
    display_image()
    login_stat()
    copy_right_img()

def show_predictions_after_delay():
    show_predictions()

def show_predictions():
    register_form.place_forget()
    home.place_forget()
    registration.place_forget()
    prediction.place(x=0,y=0)

def show_registrations():
    register_form.place_forget()
    home.place_forget()
    prediction.place_forget()
    if logged_in==False:
        registration.place(x=0,y=0)
    else:
        show_succeed_login()

def show_succeed_login():
    home.place_forget()
    register_form.place_forget()
    prediction.place_forget()
    registration.place_forget()
    success_login.place(x=0,y=0)
    log_image()

def registration_form():
    home.place_forget()
    prediction.place_forget()
    registration.place_forget()
    success_login.place_forget()
    register_form.place(x=0,y=0)

# ******************************GUI DESIGNING*************************
root = Tk()
root.title("Used Car Price Generator")
root.geometry("1270x720")
root.resizable(False, False)

#FRAMES
success_login = Frame(root,height=720,width=1272)
register_form = Frame(root,height=720,width=1272)
home = Frame(root,height=720,width=1272)
prediction = Frame(root,height=720,width=1272)
registration = Frame(root,height=720,width=1272)
ownership = Frame(root,height=30,width=1272,bg="#333333")
ownership.place(x=0,y=690)
image = Frame(home,height=250,width=1272)
image.place(x=0,y=168)
navbar = Frame(root,height=130,width=1272,bg="#8eecf5")
navbar.place(x=0,y=0)
navbar_buttons = Frame(root,height=38,width=1272,bg="#333333")
navbar_buttons.place(x=0,y=130)

#LABELS
title = Label(root,text="USED CARS PRICE PREDICTOR",font=("Montserrat",61,"bold","italic"),fg="#333333",bg="#8eecf5").place(x=10,y=15)
ownership_label = Label(ownership,text="Copyright © | Developed By Muhammad Ahmed | All Rights Reserved | 2023",bg="#333333",fg="white",font=("Montserrat",13,"bold")).place(x=310,y=2)
image_label = Label(image)
log_image_label = Label(success_login)
copyright_image = Label(home)
brand_l = Label(prediction,text="① ENTER BRAND OF CAR:",font=("Montserrat",18,"bold"),fg="#333333").place(x=80,y=250)
fuel_l = Label(prediction,text="② ENTER FUEL TYPE:",font=("Montserrat",18,"bold"),fg="#333333").place(x=80,y=300)
km_d_l = Label(prediction,text="③ ENTER MILEAGE OF CAR: ",font=("Montserrat",18,"bold"),fg="#333333").place(x=80,y=350)
car_model_l = Label(prediction,text="④ ENTER MODEL OF CAR:",font=("Montserrat",18,"bold"),fg="#333333").place(x=80,y=400)
reg_city_l = Label(prediction,text="⑤ ENTER REGISTERED CITY:",font=("Montserrat",18,"bold"),fg="#333333").place(x=80,y=450)
year_l = Label(prediction,text="⑥ ENTER REGISTRATION YEAR:",font=("Montserrat",18,"bold"),fg="#333333").place(x=80,y=500)
predict_val_l = Label(prediction,text="",font=("Montserrat",25,"bold","italic"),fg="#333333")
predict_val_l.place(x=200,y=600)
uname_l= Label(registration,text=" ENTER USERNAME",font=("Montserrat",18,"bold"),fg="#333333").place(x=100,y=300)
pass_l= Label(registration,text=" ENTER PASSWORD",font=("Montserrat",18,"bold"),fg="#333333").place(x=100,y=400)
not_reg_l = Label(registration,text="Not a Registred User?",font=("Montserrat",11,"bold"),fg="#333333").place(x=300,y=550)
availablity_check = Label(registration,font=("Montserrat",11,"bold"),fg="red")
availablity_check.place(x=500,y=530)
availablity_reg_check = Label(register_form,font=("Montserrat",11,"bold"),fg="blue")
availablity_reg_check.place(x=650,y=560)
success_login_l = Label(success_login,text="LOGGED IN SUCCESFULLY\nTHANKS FOR BEING A MEMBER",font=("Montserrat",35,"bold","italic"),fg="#333333")
success_login_l.place(x=260,y=430)
uname_reg_l = Label(register_form,text="① ENTER USERNAME:",font=("Montserrat",18,"bold"),fg="#333333").place(x=80,y=250)
fname_reg_l = Label(register_form,text="⑤ ENTER FULL NAME:",font=("Montserrat",18,"bold"),fg="#333333").place(x=80,y=300)
pass_reg_l = Label(register_form,text="② ENTER NEW PASSWORD:",font=("Montserrat",18,"bold"),fg="#333333").place(x=80,y=350)
phn_reg_l = Label(register_form,text="③ ENTER PHONE NUMBER: ",font=("Montserrat",18,"bold"),fg="#333333").place(x=80,y=400)
email_reg_l = Label(register_form,text="④ ENTER EMAIL ADDRESS:",font=("Montserrat",18,"bold"),fg="#333333").place(x=80,y=450)
login_status= Label(root,font=("Montserrat",10,"bold","italic"),fg="#333333")
login_status.place(x=1050,y=688)

#ENTRIES
brand_e = Entry(prediction,width=35,font=("Montserrat",15,"bold","italic"),bg="#8eecf5",fg="#333333")
brand_e.place(x=540,y=252)
fuel_e = Entry(prediction,width=35,font=("Montserrat",15,"bold","italic"),bg="#8eecf5",fg="#333333")
fuel_e.place(x=540,y=302)
km_d_e = Entry(prediction,width=35,font=("Montserrat",15,"bold","italic"),bg="#8eecf5",fg="#333333")
km_d_e.place(x=540,y=352)
car_model_e = Entry(prediction,width=35,font=("Montserrat",15,"bold","italic"),bg="#8eecf5",fg="#333333")
car_model_e.place(x=540,y=402)
reg_city_e = Entry(prediction,width=35,font=("Montserrat",15,"bold","italic"),bg="#8eecf5",fg="#333333")
reg_city_e.place(x=540,y=452)
year_e = Entry(prediction,width=35,font=("Montserrat",15,"bold","italic"),bg="#8eecf5",fg="#333333")
year_e.place(x=540,y=502)
uname_e = Entry(registration,width=35,font=("Montserrat",15,"bold","italic"),bg="#8eecf5",fg="#333333")
uname_e.place(x=400,y=305)
pass_e = Entry(registration,width=35,font=("Montserrat",15,"bold","italic"),bg="#8eecf5",fg="#333333")
pass_e.place(x=400,y=405)
uname_reg_e = Entry(register_form,width=35,font=("Montserrat",15,"bold","italic"),bg="#8eecf5",fg="#333333")
uname_reg_e.place(x=540,y=252)
fname_reg_e = Entry(register_form,width=35,font=("Montserrat",15,"bold","italic"),bg="#8eecf5",fg="#333333")
fname_reg_e.place(x=540,y=302)
pass_reg_e = Entry(register_form,width=35,font=("Montserrat",15,"bold","italic"),bg="#8eecf5",fg="#333333")
pass_reg_e.place(x=540,y=352)
phn_reg_e = Entry(register_form,width=35,font=("Montserrat",15,"bold","italic"),bg="#8eecf5",fg="#333333")
phn_reg_e.place(x=540,y=402)
email_reg_e = Entry(register_form,width=35,font=("Montserrat",15,"bold","italic"),bg="#8eecf5",fg="#333333")
email_reg_e.place(x=540,y=452)


#BUTTON
home_button = Button(navbar_buttons,text='  HOME  PAGE',width=41,font=("Montserrat",15,"bold","italic"),bg="#333333",fg="white",command=show_home)
home_button.place(x=-65,y=0)
predict_button = Button(navbar_buttons,text='PRICE  PREDICTOR',width=37,font=("Montserrat",15,"bold","italic"),bg="#333333",fg="white",command=show_predictions)
predict_button.place(x=430,y=0)
register_button = Button(navbar_buttons,text='REGISTER   /   LOGIN',width=35,font=("Montserrat",15,"bold","italic"),bg="#333333",fg="white",command=show_registrations)
register_button.place(x=850,y=0)
predict_inside_button = Button(prediction,text='GENERATE PREDICTION',width=25,font=("Montserrat",15,"bold","italic"),bg="#333333",fg="white",command=model_pred)
predict_inside_button.place(x=577,y=545)
login_button = Button(registration,text='LOG IN',width=20,font=("Montserrat",15,"bold","italic"),bg="#333333",fg="white",command=login_db_manage)
login_button.place(x=470,y=485)
register_button = Button(registration,text='REGISTER',width=20,font=("Montserrat",15,"bold","italic"),bg="#333333",fg="white",command=registration_form)
register_button.place(x=370,y=580)
register_me_button = Button(register_form,text='REGISTER ME!',width=20,font=("Montserrat",15,"bold","italic"),bg="#333333",fg="white",command=register_db_manage)
register_me_button.place(x=612,y=500)


show_home()
root.mainloop()
conn.commit()
cursor.close()
conn.close()
