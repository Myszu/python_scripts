import logging
import sys
from time import sleep, time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from progress import Progress

class Crawler():
    def __init__(self) -> None:
        super().__init__()
        logging.basicConfig(format=f'%(asctime)s | %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO , filename='crawling-log.log')
        
        self.progress = Progress()
        
        self.options = webdriver.FirefoxOptions()
        
        self.options.add_argument("--headless")
        self.options.add_argument("--width=1920")
        self.options.add_argument("--height=1080")
        
        logging.info('Program initialized.')
        self.browser = webdriver.Firefox(options=self.options)
        self.wait = WebDriverWait(self.browser, 15)
        self.actions = ActionChains(self.browser)
        
        self.matches = []
        self.output = {}
        self.visited = []
        self.times = []
        self.max_dept = 1
        self.output_file = 'output.txt'
        

    def run(self) -> None:
        self.url = input('Input the initial link you want to investigate: ')
        self.domain = self.url.split('/')[2]
        logging.info(f'Reaching {self.url}.')
        print(f'Reaching {self.url} website.')
        self.browser.get(self.url)
        sleep(1)
        
        try:
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        except:
            logging.exception("Can't reach endpoint website or no links found.")
            retry = input("Couldn't reach your website or no further links found on. Do you wish to retry? (\"y\" to confirm): ")
            if retry == 'y':
                self.run()
                
        logging.info('Initial website reached. Finding all links on it.')
        print('Initial website reached. Finding all links on it.')
        try:
            self.links = list(set([link.get_attribute('href') for link in self.browser.find_elements(By.TAG_NAME, 'a')]))
        except:
            self.links = []
        
        if not self.links:
            logging.warning('No links found.')
            print('No sub-websites, nor links found on initial website.')
            self.stop(1)
            
        self.keywords = input('Input keywords (e.g. domain names seperated with comas) that will determine match of what you are looking for: ').split(',')
        logging.info(f'Inputted keywords: {','.join(self.keywords)}.')
        
        if not self.keywords:
            logging.warning('No keywords inputted.')
            print('No keywords inserted, therefore nothing to find.')
            self.stop(1)
            
        try:
            self.max_dept = int(input('How many deep in sub-pages do you want to go? 1 or less means no subpages, in most usecases 2 is enough. Type a number: '))
        except:
            self.max_dept = 1
            
        if self.max_dept < 1:
            self.max_dept = 1
        
        self.links = self.sweep(self.url, self.links)
        print(f'Found {len(self.links)} initial sub-websites and {len(self.matches)} initial matches.')
            
        self.crawl(self.links)
        
        if self.matches:    
            self.save()
        self.stop(0)
        
    
    def crawl(self, links: list, dept: int = 1) -> None:
        if dept > self.max_dept: return
        if dept == 1:
            logging.info('Beginning initial crawl.')
            print('Beginning initial crawl.')
        else:
            logging.info(f'Crawling on level {dept}.')
            print(f'Crawling one level deeper. Going to level {dept}.')
            
        inner_links = []
        for i, link in enumerate(links):
            start = time()
            if link not in self.visited and str(link).find(self.domain)>=0:
                self.visited.append(link)
                try:
                    self.browser.get(link)
                    
                    sleep(1)
                    
                    try:
                        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
                        temp = self.sweep(link, list(set([link.get_attribute('href') for link in self.browser.find_elements(By.TAG_NAME, 'a')])))
                        inner_links.extend(temp)
                    except:
                        logging.exception(f"Can't find any links on {link} website.")
                except:
                    logging.exception(f"Can't reach {link} website.")
            self.times.append(time()-start)
            self.progress.Update(i, len(links), self.times, f'{len(self.matches)} match(es) found')
        
        print()
        self.times.clear()
        dept += 1
        if inner_links:
            self.crawl(inner_links, dept)
        
        
    def sweep(self, source: str, links: list) -> list:
        logging.info('Filtering list of links.')
        output = []
        for link in links:
            try:
                if link.find(self.domain)>=0 and not link.find('?format=')>=0:
                    output.append(link)
                elif self.search(link):
                    self.matches.append(link)
                    if self.output.get(source) is None:
                        self.output[source] = []
                    self.output[source].append(link)
            finally:
                continue
        return output
        
        
    def search(self, link: str) -> bool:
        for keyword in self.keywords:
            if link.find(keyword)>=0:
                return True
        return False
    
    
    def save(self) -> None:
        logging.exception(f'Saving matches to {self.output_file}.')
        print(f'Saving matches to {self.output_file}')
        try:
            f = open(self.output_file, 'a')
            for key, value in self.output.items():
                f.write(f'{key}: {','.join(value)}\n')
            f.close()
        except:
            logging.exception('Error on saving the file.')
            print(f'Couldn\'t create/save {self.output_file} file.')
            self.stop(1)
        
        
    def stop(self, code) -> None:
        if self.browser:
            self.browser.quit()
        for i in range(5, 0, -1):
            if self.matches:
                print(f'Crawling finished. Closing in {i} seconds.', end='\r')   
            else:
                print(f'Crawling finished. Output saved to {self.output_file}. Closing in {i} seconds.', end='\r')
            sleep(1)
        print()
                
        sys.exit(code)
        
        
if __name__ == "__main__":
    app = Crawler()
    app.run()