from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from random_username.generate import generate_username
from selenium.webdriver.common.action_chains import ActionChains
from random import randrange
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import itertools
import discord
import pyautogui


username = generate_username(1)[0]

password = "password"

def get_text_excluding_children(driver, element):
    return driver.execute_script("""
    return jQuery(arguments[0]).contents().filter(function() {
        return this.nodeType == Node.TEXT_NODE;
    }).text();
    """, element)


driver = webdriver.Chrome()
driver.maximize_window()

driver.get('https://www.guerrillamail.com/#')
time.sleep(2)


elem = Select(driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/span[1]/select'))
elem.select_by_visible_text('pokemail.net')

time.sleep(2)


elem = driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/span[1]/span')

email = get_text_excluding_children(driver, elem)
email += "@pokemail.net"


print(email)
print(username)
print(password)

window_before = driver.window_handles[0]


driver.execute_script('''window.open("https://signin.ea.com/p/originX/create?execution=e2083486491s1&initref=https%3A%2F%2Faccounts.ea.com%3A443%2Fconnect%2Fauth%3Fresponse_type%3Dcode%26client_id%3DORIGIN_SPA_ID%26display%3DoriginXWeb%252Fcreate%26locale%3Den_US%26release_type%3Dprod%26redirect_uri%3Dhttps%253A%252F%252Fwww.origin.com%252Fviews%252Flogin.html","_blank");''')
time.sleep(5)

window_after = driver.window_handles[1]
driver.switch_to.window(window_after)

elem = Select(driver.find_element_by_xpath('/html/body/div[1]/div[1]/section/form/div[1]/div[1]/div[2]/div/div/div[1]/select'))

date = ['January','February','March','April','May','June','July','August','September','October','November','December']
ran = randrange(1,12)

elem.select_by_visible_text(date[ran])

time.sleep(1)

elem = Select(driver.find_element_by_xpath('/html/body/div[1]/div[1]/section/form/div[1]/div[1]/div[2]/div/div/div[2]/select'))
elem.select_by_visible_text(str(randrange(1,20)))

time.sleep(1)

elem = Select(driver.find_element_by_xpath('/html/body/div[1]/div[1]/section/form/div[1]/div[1]/div[2]/div/div/div[3]/select'))
elem.select_by_visible_text(str(randrange(1967,2000)))

time.sleep(1)

elem = driver.find_element_by_xpath('/html/body/div[1]/div[1]/section/form/div[1]/div[2]/span/label')

time.sleep(1)


action = webdriver.common.action_chains.ActionChains(driver)
action.move_to_element_with_offset(elem, 10, 10)
action.click()
action.perform()

time.sleep(1)

driver.find_element_by_xpath('/html/body/div[1]/div[1]/section/form/div[1]/div[3]/a').click()

time.sleep(1)


driver.find_element_by_xpath('/html/body/div[1]/div[1]/section/form/div[2]/div[1]/div[1]/div/input').send_keys(email)

time.sleep(3.1)

driver.find_element_by_xpath('/html/body/div[1]/div[1]/section/form/div[2]/div[1]/div[4]/div/input').send_keys(password)

time.sleep(4.6)

driver.find_element_by_xpath('/html/body/div[1]/div[1]/section/form/div[2]/div[2]/div[1]/div/input').send_keys(username)

time.sleep(2)

driver.find_element_by_xpath('/html/body/div[1]/div[1]/section/form/div[2]/div[4]/a').click()

time.sleep(2)

elem = Select(driver.find_element_by_xpath('/html/body/div[1]/div[1]/section/form/div[3]/div[1]/div[1]/span/select'))
elem.select_by_visible_text('What elementary school did you attend?')

time.sleep(1)

driver.find_element_by_xpath('/html/body/div[1]/div[1]/section/form/div[3]/div[1]/div[2]/div/input').send_keys("St. Vincent de Paul")

time.sleep(1)

screenWidth, screenHeight = pyautogui.size()

pyautogui.click(screenWidth/2, screenHeight/2+300)

time.sleep(2)

driver.switch_to.window(window_before)

#find seccode from email

elem = None

while(not elem):
    time.sleep(1)
    elem = driver.find_elements_by_xpath("//*[contains(text(), 'Your EA Security Code is')]")

seccode = get_text_excluding_children(driver, elem)
seccode = seccode.split()[5]


time.sleep(2)

driver.switch_to.window(window_after)

#verixpath
driver.find_element_by_xpath('/html/body/div[1]/form/div/section/div[2]/input').send_keys(seccode)
time.sleep(1)

#confim xpaths
driver.find_element_by_xpath('/html/body/div[1]/form/div/section/a[2]').click()


one = "Account setup complete"
two = "EMAIL: " + email
three = "USERNAME: " + username
four = "PASSWORD: " + password

print(one)
print(two)
print(three)
print(four)


TOKEN = 'Discord Token'

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    apex = client.get_channel('688419372636831785')
    await client.send_message(apex, one)
    await client.send_message(apex, two)
    await client.send_message(apex, three)
    #await client.send_message(apex, four)
    time.sleep(5)
    driver.close()
    driver.close()
    exit()
    
client.run(TOKEN)


driver.close()

input("Press ENTER to exit")
