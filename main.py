# for SMS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
# For GUI
import tkinter as tk
# for Run Python Program
from datetime import datetime, timedelta
import re
import os

# for Administrator permissions
import ctypes
import sys

def run_as_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        # Prepare the command line arguments
        script_path = os.path.abspath(__file__)
        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])  # Properly handle arguments with spaces
        
        print("Requesting admin privileges...")
        
        # Attempt to elevate privileges
        response = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script_path}" {params}', None, 1)
        
        if response <= 32:  # If ShellExecuteW fails, it returns a value less than 32
            messagebox.showerror("Permission Denied", "Failed to obtain administrator privileges.")
            sys.exit(1)
        else:
            sys.exit()  


def block_website(website):
    hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
    
    result = "\n"
    flag = 0;
    
    if len(website) != 0:
        my_list = split_website(website)

        
        for website in my_list:
            with open(hosts_path , 'r+') as file:
                file_read = file.read()
                flag = 0
                if website not in file_read:
                    file.write(f"{website}\n")
                    flag = 1
                if flag == 0:
                    result += (f"\t* {website} already blocked.\n")

                if flag == 1:
                    result += f"\t*{website} successfully blocked.\n"
                file.close()
        

        os.system("ipconfig /flushdns")
        result  = re.sub(r"127.0.0.1 ", "", result)
        display_result(result)
    else:
        result = "\t* Please, At First Insert Your URL."
        display_result(result)

def unblock_website(websites):
    hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
    flag = 0
    result = ""
    for website in websites:
        with open(hosts_path,'r') as file:
            contents = file.read()
            flag = 0
            if website in contents:
                contents = contents.replace(f"{website}\n", "")
                flag = 1
                with open(hosts_path,'w') as file:
                    file.write(contents)

            if flag == 0:
                result += (f"\t* {website} already unblocked.\n")

            if flag == 1:
                result += f"\t*{website} successfully unblocked.\n"
            
            file.close()
    result  = re.sub(r"127.0.0.1 ", "", result)
    unblock_site_page()
    unblock_display_result(result)

def unblock_check(websites):
    hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
    flag = False;
    with open(hosts_path, 'r') as file:
        file_contents = file.read()
        for website in websites:
            if website in file_contents:
                flag = True
    return flag

def unblock_match(websites):
    result = ''
    if len(websites) != 0:
        websites = split_website(websites)
        if unblock_check(websites):
            result = "URL Found.\nSending Email. Please Wait."
            unblock_display_result(result)
            if email_time(websites):
                code_sending_time = datetime.now()  
                unblock_confirm(websites, code_sending_time)
                result = 'Email Send'
            else:
                result = '\t Email Not Send.'
        else:
            result = '\t*Website already unblocked.'
    else:
        result = "\t*Please, At First Insert Your URL."
    unblock_display_result(result)

def check_confirmation_code(code, websites, code_sending_time):
    code.replace(' ','')
    code = int(code)
    new_time = code_sending_time + timedelta(minutes=2)
    if new_time > datetime.now():
        if rendom_number_generator.confirmation_code == code:
            unblock_website(websites)
        else:
            unblock_site_page()
            unblock_display_result("Code is not corrent. Try Again.")
    else:
        unblock_site_page()
        unblock_display_result("Time is out. Try Again.")

def rendom_number_generator():
    random_number = random.randrange(100000, 1000000)
    rendom_number_generator.confirmation_code = random_number
    return random_number
def email_time(website):
    # Email configuration
    sender_email = "*******************"
    receiver_email = "******************"
    subject = "WebsiteBlockerApp Software Notification"
    random_number = rendom_number_generator()
    website = " ".join(map(str,website))
    website  = re.sub(r"127.0.0.1 ", "", website)
    website  = re.sub(r" ", ", ", website)
    message = f"You can unblock {website} website using {random_number} code."

    # SMTP server configuration (for Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "*********************"
    smtp_password = "***************"
    # Create a multipart message and set the headers
    email_message = MIMEMultipart()
    email_message["From"] = sender_email
    email_message["To"] = receiver_email
    email_message["Subject"] = subject
    # Attach the message to the email body
    email_message.attach(MIMEText(message, "plain"))

    # Create a secure SSL/TLS connection with the SMTP server
    smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
    smtp_connection.starttls()

    # Log in to your email account
    smtp_connection.login(smtp_username, smtp_password)

    # Send the email
    smtp_connection.sendmail(sender_email, receiver_email, email_message.as_string())

    # Close the SMTP connection
    smtp_connection.quit()
    return 1



def domain_extention_check(website):
    domain_extentions = ['.com','.net','.org', '.io', '.co', '.ai', '.co.uk', '.ca','.dev', '.me']
    for extention in domain_extentions:
        if extention in website:
            return extention

def split_website(website):
    redirect_ip = '127.0.0.1'

    website  = re.sub(r" ", "", website)
    website  = re.sub(r"https:", "", website)
    website  = re.sub(r"http:", "", website)
    my_list = website.split(",")
    list = []

    for website in my_list:
        extention = domain_extention_check(website)
        print(extention)
        website = website.split(extention)
        # Keep only the first part of the split URL
        website = website[0] + extention
        website  = re.sub(r"/", "", website)
        url = (f'{redirect_ip} {website}')
        list.append(url)
    return list




root = tk.Tk()
root.geometry("525x400")
root.title("Website Blocker App")

def home_page():
    home_frame = tk.Frame(main_frame)
    lb = tk.Label(home_frame, text='Home Page\n\nPage:1',font=('Bold',30))
    lb.pack()
    home_frame.pack(pady=20)

def block_site_page():
    block_site_frame = tk.Frame(main_frame)
    # block_site_page.block_site_frame = block_site_frame  # Assign the frame to the function as an attribute
    lb = tk.Label(block_site_frame, text='Block Your Website',font=('Bold',14))
    lb.pack()   
    url_input_label = tk.Label(block_site_frame, text="Website URL", font=11)
    url_input_label.pack()
    url_input = tk.Entry(block_site_frame)
    url_input.pack()
    block_btn = tk.Button(block_site_frame, text='Block', font=12,command=lambda:block_website(url_input.get()))
    block_btn.pack()
    result = tk.Label(block_site_frame, text='')
    block_site_page.result = result
    result.pack()

    block_site_frame.pack(pady=20)

def display_result(result):
    block_site_page.result.config(text=result)
def unblock_display_result(result):
    unblock_site_page.result.config(text=result)
def unblock_site_page():
    delete_pages()
    unblock_site_frame = tk.Frame(main_frame)
    lb = tk.Label(unblock_site_frame, text='Unblock Your Website',font=('Bold',14))
    lb.pack()
    url_input_label = tk.Label(unblock_site_frame, text="Website URL", font=11)
    url_input_label.pack()
    url_inupt = tk.Entry(unblock_site_frame)
    url_inupt.pack()
    unblock_btn = tk.Button(unblock_site_frame, text="Unblock", font=12, command=lambda:unblock_match(url_inupt.get()))
    unblock_btn.pack()
    result = tk.Label(unblock_site_frame, text='')
    unblock_site_page.result = result
    result.pack()
    unblock_site_frame.pack(pady=20)

def unblock_confirm(websites, code_sending_time):
    delete_pages()
    unblock_confirm_frame = tk.Frame(main_frame)
    lb = tk.Label(unblock_confirm_frame, text='Unblock Code Confirmation',font=('Bold',14))
    lb.pack()
    confirmation_label = tk.Label(unblock_confirm_frame, text="Inter confirmation Code", font=11)
    confirmation_label.pack()
    code_inupt = tk.Entry(unblock_confirm_frame)
    code_inupt.pack()
    confirm_btn = tk.Button(unblock_confirm_frame, text="Confirm", font=12, command=lambda: check_confirmation_code(code_inupt.get(), websites, code_sending_time))
    confirm_btn.pack()
    result = tk.Label(unblock_confirm_frame, text='')
    unblock_site_page.result = result
    result.pack()
    alart = tk.Label(unblock_confirm_frame, text='Inter Your Code within 2 minutes.')
    alart.pack()
    unblock_confirm_frame.pack(pady=20)
    
def about_page():
    about_frame = tk.Frame(main_frame)
    lb = tk.Label(about_frame, text='About Page\n\nPage:4',font=('Bold',30))
    lb.pack()
    about_frame.pack(pady=20)


def delete_pages():
    for frame in main_frame.winfo_children():
        frame.destroy()

def hide_indicate():
    home_indicate.config(bg='#c3c3c3')
    block_site_indicate.config(bg='#c3c3c3')
    unblock_site_indicate.config(bg='#c3c3c3')
    about_indicate.config(bg='#c3c3c3')

def indicate(lb, page):
    hide_indicate()
    lb.config(bg='#158aff')
    delete_pages()
    page()

options_frame = tk.Frame(root, bg="#c3c3c3")

home_btn = tk.Button(options_frame, text='Home', font=('Bold',12), fg="#158aff", bd=0, bg="#c3c3c3", command=lambda:indicate(home_indicate, home_page))
home_btn.place(x=10, y=40)
home_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
home_indicate.place(x=3, y=40, width=5, height=30)

block_site_btn = tk.Button(options_frame, text='Block Site', font=('Bold',12), fg="#158aff", bd=0, bg="#c3c3c3", command=lambda:indicate(block_site_indicate, block_site_page))
block_site_btn.place(x=10, y=80)
block_site_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
block_site_indicate.place(x=3, y=80, width=5, height=30)


unblock_site_btn = tk.Button(options_frame, text='Unblock Site', font=('Bold',12), fg="#158aff", bd=0, bg="#c3c3c3", command=lambda:indicate(unblock_site_indicate, unblock_site_page))
unblock_site_btn.place(x=10, y=120)
unblock_site_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
unblock_site_indicate.place(x=3, y=120, width=5, height=30)

about_btn = tk.Button(options_frame, text='About', font=('Bold',12), fg="#158aff", bd=0, bg="#c3c3c3", command=lambda:indicate(about_indicate, about_page))
about_btn.place(x=10, y=160)
about_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
about_indicate.place(x=3, y=160, width=5, height=30)

options_frame.pack(side=tk.LEFT)
options_frame.pack_propagate(False)
options_frame.configure(width=125, height=400)


main_frame = tk.Frame(root, highlightbackground='black', highlightthickness=2)
main_frame.pack(side=tk.LEFT)
main_frame.pack_propagate(False)
main_frame.configure(height=400, width=500)
run_as_admin()
root.mainloop()