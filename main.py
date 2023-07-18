from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from PIL import Image
from io import BytesIO
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg

config = Cfg.load_config_from_name("vgg_transformer")
config["cnn"]["pretrained"] = False
config["device"] = "cpu"
detector = Predictor(config)

url = "http://tracuudiem.thitotnghiepthpt.edu.vn/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

id = 0

while True:
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    print(url)

    id += 1
    string_id = str(id).rjust(8, "0")

    try:
        input_id = driver.find_element(By.ID, "identifyNumber")
        input_id.send_keys(string_id)

        image_captcha = driver.find_element(By.ID, "imgCaptcha")
        image_location = image_captcha.location
        size = image_captcha.size
        png = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(png))
        left = image_location["x"]
        top = image_location["y"]
        right = image_location["x"] + size["width"]
        bottom = image_location["y"] + size["height"]
        image = image.crop((left, top, right, bottom))
        string_captcha = detector.predict(image)

        input_captcha = driver.find_element(By.ID, "strCaptcha")
        input_captcha.send_keys(string_captcha)
        input_captcha.send_keys(Keys.RETURN)
        time.sleep(10000)
    except:
        print("hahaha")

    break
