from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def scrape_date_from(areaCode_, areaName_, year_, month_, date_):
    chrome_options = Options()
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"https://www.lotterypost.com/results/{areaCode_}/{year_}/{month_}/{date_}")
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.resultsdrawing")))
    
    results = driver.find_elements(By.CSS_SELECTOR, "div.resultsdrawing")
    scrapedData = []
    
    for result in results:
        try:        
            title = result.find_element(By.CSS_SELECTOR, "h2")
            date = result.find_element(By.CSS_SELECTOR, "time")
            nums = result.find_element(By.CSS_SELECTOR, "ul.resultsnums")

        except Exception:
            break

        numList = []
        for num in nums.find_elements(By.CSS_SELECTOR, "li"):
            numList.append(num.text)
                
        scrapedData.append({
            'area': areaName_,
            'title': title.text,
            'date': date.text,
            'nums': numList
        })
    
    driver.quit()
    return scrapedData