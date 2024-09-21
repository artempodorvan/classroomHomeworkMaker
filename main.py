import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import time
import cloudinary
import cloudinary.uploader
import GenerateImage as gm

# Configure Cloudinary
cloudinary.config(
    cloud_name='dherxmyiz',
    api_key='894999243925242',
    api_secret='JRvvc7bCUk8YVO8yVeYu2Xu0bV0'
)

# Define course URLs
course_url = {
    'geo': '/c/NzA4MjQyNTU2Mjkw',
    'his_ukr': '/c/NzA3NTA3OTg0Mjky',
    'his_vse': '/c/NzA3NTA5MzA3NjI0',
    'algebra': '/c/NzA4NjMxOTQyOTk1',
    'geomet': '/c/NzA4NjMzNzYxODc5',
    'ukr_mova': '/c/NzA4MzA0MzI0NzQz',
    'ukr_lit': '/c/NzA4MzAzMTg3NDc0',
    'info': '/c/NzA3OTcwMTY4MzIx',
    'finance': '/c/NzA3MTU5NjgwODMy',
    'zaruba': '/c/NzA4MjQ5ODM4NTQ2',
    'eng': '/c/NzA3MjU3NjMwMjc5',
    'fisika': '/c/NzA3OTc1ODQ0NTA5',
    'himiya': '/c/NzA3ODYyNDE2MTU0',
    'bio': '/c/NzA3NzIyOTUwODkz'
}

# Get the folder path where the image will be saved
generated_img_path = input('Enter the path to the folder where you want to save the image: ')

# Generate the handwritten image and save it in the specified folder
input_text = "закон центра тяжіння..."
handwritten_paper = gm.generate_handwritten_image(input_text)
image_save_path = os.path.join(generated_img_path, "generated_handwritten_image.jpg")
gm.place_paper_on_table(handwritten_paper, 'desk.jpg', generated_img_path)

# Get subjects input from the user
subjects_input = input("Enter subjects separated by commas (e.g., geo, algebra): ")

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open Google Classroom
driver.get("https://classroom.google.com/")

# Log in to Google Classroom
sign_in_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[@class='gfe-button gfe-button--medium-emphasis gfe-button--center-align']"))
)
sign_in_button.click()

time.sleep(5)

pyautogui.write("podorvan@i18.pp.ua")
pyautogui.press("enter")

time.sleep(5)
pyautogui.write("Artem838podorvan")
pyautogui.press("enter")

time.sleep(5)

# Split subjects and clean up whitespace
subjects = [subj.strip() for subj in subjects_input.split(',')]

time_offset = -60
time_offset1 = -30

# Switch to the last opened window
window_handles = driver.window_handles
driver.switch_to.window(window_handles[-1])

time.sleep(0.5)

for subject in subjects:
    if subject in course_url:
        driver.get(f"https://classroom.google.com{course_url[subject]}")
    else:
        print(f'There is no such subject as {subject}')
        continue

    time.sleep(5)

    task_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.qhnNic.LBlAUc.Aopndd.TIunU.xWw7yd.h7Ww0.DkDwHe'))
    )

    task_element.click()

    time.sleep(5)

    subject_folder = os.path.join(subject)
    if not os.path.exists(subject_folder):
        print(f"No folder found for subject {subject}. Skipping...")
        continue

    for image_file in os.listdir(subject_folder):
        if image_file.endswith(".jpg") or image_file.endswith(".png"):
            time_offset += 60
            time_offset1 += 30

            # Click to add homework
            pyautogui.moveTo(1100, 410 + time_offset, duration=0.5)
            pyautogui.click()

            time.sleep(0.5)

            # Choose URL option
            pyautogui.moveTo(1100, 530 + time_offset, duration=0.5)
            pyautogui.click()

            time.sleep(0.5)

            # Click the URL field
            pyautogui.moveTo(700, 600, duration=0.5)
            pyautogui.click()

            time.sleep(0.5)

            # Upload the image to Cloudinary and get the URL
            response = cloudinary.uploader.upload(os.path.join(subject_folder, image_file))
            pyautogui.write(response['url'])

            time.sleep(0.5)

            # Add URL
            pyautogui.moveTo(750, 715, duration=0.5)
            pyautogui.click()

            time.sleep(2)

    # Send homework
    pyautogui.moveTo(1100, 565 + time_offset, duration=0.5)
    pyautogui.click()

    time.sleep(2)

    # Confirm send
    pyautogui.moveTo(975, 720 + time_offset1, duration=0.5)
    pyautogui.click()

    time_offset = -60
    time_offset1 = -30

driver.quit()
