from curses.ascii import TAB
from sqlalchemy import true
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

password_mail = 'XXXX'
password_coloc = 'XXXX'

def get_driver():
	options = uc.ChromeOptions()
	options.add_argument("--no-sandbox --no-first-run --no-service-autorun --password-store=basic")
	# options.headless = True
	driver = uc.Chrome(options=options, version_main=102)
	return(driver)

def login(driver):
	driver.find_element_by_xpath("//input[@id='login']").send_keys('ROBIND')
	driver.find_element_by_xpath("//input[@id='password']").send_keys(password_coloc)
	driver.find_element_by_xpath("//button[@type='submit']").click()

def runner(driver):
	url = 'https://www.colocatere.com/fr/admin/connexion'
	driver.get(url)
	login(driver)
	driver.get("https://www.colocatere.com/fr/admin/prospects")
	list_prospects = []
	try:
		i = 1
		while(True):
			table = driver.find_element_by_xpath(f'//*[@id="general-table"]/tbody/tr[{i}]')
			s = str(table.text).split('\n')
			
			if len(s) < 6:
				list_prospects.append(s)
				print(s)
				# bouton de suivi
				# driver.find_element_by_xpath(f'/html[1]/body[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/table[1]/tbody[1]/tr[{i}]/td[5]/div[1]/a[2]/i[1]').click()
				# driver.get("https://www.colocatere.com/fr/admin/prospects")
				print('\n')
			i+=1
	except:
		print('Finished scrapping the prospect table.')
	return (list_prospects)

def send_mail(driver, list_prospects):
	url = 'https://outlook.office.com/'
	driver.get(url)
	driver.find_element_by_xpath("//input[@id='i0116']").send_keys('robin.dehouck@colocatere.fr')
	time.sleep(1)
	driver.find_element_by_xpath("//input[@id='idSIButton9']").click()
	time.sleep(1)
	driver.find_element_by_xpath("//input[@id='i0118']").send_keys(password_mail)
	time.sleep(1)
	driver.find_element_by_xpath("//input[@id='idSIButton9']").click()
	time.sleep(1)
	driver.find_element_by_xpath("//input[@id='idSIButton9']").click()
	time.sleep(1)
	driver.find_element_by_xpath("//span[@id='id__9']").click()
	for prospect in list_prospects:
		time.sleep(1)
		driver.find_element_by_xpath("//input[@aria-label='À']").send_keys(prospect[3])
		action_object = ActionChains(driver)
		action_object.send_keys(Keys.TAB * 2)
		action_object.send_keys('test')
		action_object.perform()
		action_content = ActionChains(driver)
		action_content.send_keys(Keys.TAB * 1)
		action_content.send_keys(f'Dear {prospect[0]},\n\nThis is a test.')
		action_content.perform()
		time.sleep(10)
		i = 0
		lock = 0
		while lock == 0 or lock == 1:
			try:
				new_mail = driver.find_element_by_xpath(f"//span[@id='id__{i}']")
				i+=1
				lock += 1
			except:
				print(i)
				i+=1
		new_mail.click()



if __name__ == "__main__":
	driver = get_driver()
	list_prospects = runner(driver)
	send_mail(driver, list_prospects)