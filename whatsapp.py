import os
import shutil
import time
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import queue
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import qrcode

# Queue for storing message details
message_queue = queue.Queue()
sending = threading.Event()

def generate_qr_code():
    global driver, qr_image_label
    wp = "WP"
    CHROME_PROFILE_PATH = f"user-data-dir=C:/Users/jayuu/AppData/Local/Google/Chrome/User Data/Default/{wp}"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(CHROME_PROFILE_PATH)
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://web.whatsapp.com")
    time.sleep(20)

    try:
        element = driver.find_element(By.XPATH, '//div[@class="_akau"]')
        time.sleep(1)
        code = element.get_attribute("data-ref")
        print('QR code:', code)

        qr = qrcode.QRCode(version=3, box_size=20, border=10, error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(code)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("qr_code.png")

        qr_img = Image.open("qr_code.png")
        qr_img = qr_img.resize((200, 200), Image.LANCZOS)
        qr_photo = ImageTk.PhotoImage(qr_img)

        if qr_image_label:
            qr_image_label.config(image=qr_photo)
            qr_image_label.image = qr_photo
        else:
            qr_image_label = tk.Label(app, image=qr_photo)
            qr_image_label.image = qr_photo
            qr_image_label.grid(row=1, column=1, columnspan=2)

        close_button = tk.Button(app, text="Close", command=close_driver)
        close_button.grid(row=2, column=1)
    except Exception as e:
        print(f"Error fetching QR code: {e}")
        messagebox.showerror("Error", "Error fetching QR code.")
        driver.quit()

def close_driver():
    global driver, qr_image_label
    driver.quit()
    if qr_image_label:
        qr_image_label.grid_forget()
        qr_image_label = None

def sendtext(driver, text):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, '_ak1l'))
        )

        def send_keys_delayed(element, text, delay=0.1):
            for char in text:
                element.send_keys(char)
                time.sleep(delay)
        
        send_keys_delayed(element, text)
        time.sleep(5)
        element.send_keys(Keys.ENTER)
        print('Text message sent successfully!')
        time.sleep(2)
        
    except Exception as e:
        print(f"An exception occurred: {e}")
        driver.save_screenshot("error.png")
        driver.quit()

def sendmedia(driver, text, filelocation):
    if text:
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, '_ak1l'))
            )

            def send_keys_delayed(element, text, delay=0.1):
                for char in text:
                    element.send_keys(char)
                    time.sleep(delay)

            send_keys_delayed(element, text)
        except Exception as e:
            print(f"An exception occurred while sending text: {e}")
            driver.save_screenshot("error.png")
            driver.quit()

    try:
        plusbtn = driver.find_element(By.CLASS_NAME, 'x11xpdln')
        plusbtn.click()
    except Exception as e:
        print(f"Error finding + button: {e}")

    try:
        document = driver.find_element(By.XPATH, '//input[@accept="*"]')
        time.sleep(2)
        document.send_keys(filelocation)
        time.sleep(2)
    except Exception as e:
        print(f"Error in finding PDF file: {e}")

    try:
        sendbtn = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
        time.sleep(2)
        sendbtn.click()
    except Exception as e:
        print(f"Error finding send button: {e}")

    time.sleep(2)
    driver.quit()

def run_whatsapp_automation(phone, text, document, status_label, row_id):
    sending.set()
    update_status(row_id, "Sending...")

    # WebDriver setup
    CHROME_PROFILE_PATH = "user-data-dir=C:/Users/jayuu/AppData/Local/Google/Chrome/User Data/Default/WP"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(CHROME_PROFILE_PATH)
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    time.sleep(5)

    driver.get(f"https://web.whatsapp.com/send?phone={phone}")
    time.sleep(15)

    try:
        if document:
            sendmedia(driver, text, document)
        elif text:
            sendtext(driver, text)

        status_label.config(text="Message sent successfully!")
        update_status(row_id, "Sent successfully")
    except Exception as e:
        update_status(row_id, f"Failed: {str(e)}")

    sending.clear()
    driver.quit()

    if not message_queue.empty():
        next_message = message_queue.get()
        run_whatsapp_automation(*next_message)

def update_status(row_id, status):
    status_table.item(row_id, values=(status_table.item(row_id, 'values')[0], status))

# Tkinter GUI
def browse_file():
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("PDF files", "*.pdf*"), ("all files", "*.*")))
    document_entry.delete(0, tk.END)
    document_entry.insert(0, filename)

def submit():
    phone = phone_entry.get()
    text = text_entry.get("1.0", tk.END).strip()
    document = document_entry.get()

    if not phone:
        messagebox.showerror("Input Error", "Phone number is required.")
        return

    phone_entry.delete(0, tk.END)
    text_entry.delete("1.0", tk.END)
    document_entry.delete(0, tk.END)
    
    status_label.config(text="Sending...")

    row_id = status_table.insert('', 'end', values=(phone, "Queued"))

    if not sending.is_set():
        threading.Thread(target=run_whatsapp_automation, args=(phone, text, document, status_label, row_id)).start()
    else:
        message_queue.put((phone, text, document, status_label, row_id))
        update_status(row_id, "Queued")

app = tk.Tk()
app.title("WhatsApp Automation")

qr_image_label = None

# Generate QR Code Button
tk.Button(app, text="Generate QR Code", command=generate_qr_code).grid(row=0, column=1)

tk.Label(app, text="Phone Number:").grid(row=3, column=0)
phone_entry = tk.Entry(app)
phone_entry.grid(row=3, column=1)

tk.Label(app, text="Text Message:").grid(row=4, column=0)
text_entry = tk.Text(app, height=5, width=40)
text_entry.grid(row=4, column=1)

tk.Label(app, text="Document Path:").grid(row=5, column=0)
document_entry = tk.Entry(app)
document_entry.grid(row=5, column=1)
tk.Button(app, text="Browse", command=browse_file).grid(row=5, column=2)

tk.Button(app, text="Submit", command=submit).grid(row=6, column=1)

status_label = tk.Label(app, text="")
status_label.grid(row=7, column=1)

# Status table
columns = ('Phone Number', 'Status')
status_table = ttk.Treeview(app, columns=columns, show='headings')
status_table.heading('Phone Number', text='Phone Number')
status_table.heading('Status', text='Status')
status_table.grid(row=8, column=0, columnspan=3)

app.mainloop()
