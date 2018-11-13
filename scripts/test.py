from selenium import webdriver
from selenium.webdriver import ChromeOptions


options = ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1280,1024')

remote_driver_url = "/"
driver = webdriver.Chrome(
  desired_capabilities=options.to_capabilities()
)

url = "https://www.google.co.jp/"
print("Driver get to %s" % url)
driver.get(url)
driver.save_screenshot('test.png')
print("Saved test.png")

