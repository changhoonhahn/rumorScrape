"""
Scrape astro rumor mill
"""
import re
import requests
from bs4 import BeautifulSoup 
# -- toga -- 
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class rumorScrape(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box(style=Pack(direction=COLUMN))
        
        self.kwd_input = toga.TextInput(placeholder='keywords', style=Pack(width=400, flex=1))
        self.status_output = toga.MultilineTextInput(readonly=True, placeholder='', style=Pack(flex=1))

        button = toga.Button('Get Status', on_press=self.scrape)
        kwd_box = toga.Box(style=Pack(direction=ROW, padding=10))
        kwd_box.add(self.kwd_input)
        kwd_box.add(button) 
        
        status_container = toga.ScrollContainer(style=Pack(height=400, direction=COLUMN, padding=10),
                horizontal=False, vertical=False)
        status_box = toga.Box(style=Pack(width=600, height=400))
        status_box.add(self.status_output)
        status_container.content = status_box
        
        main_box.add(kwd_box)
        main_box.add(status_container) 

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def scrape(self, widget):
        self.status_output.value = self.scrape_rumormill()

    def scrape_rumormill(self): 
        ''' scrape nyt url and get ingredients and instructions 
        '''
        keyword_list = self.parse_keywords()

        r = requests.get('https://www.astrobetter.com/wiki/Rumor+Mill') 
        soup = BeautifulSoup(r.content, 'html.parser')

        # remove all href
        for a in soup.find_all('a'):
            del a['href'] 
    
        output = [] 
        for item in soup.find_all('tr'): 
            cells = item.find_all('td') 
            if len(cells) == 0: continue
            name = str(cells[0]).replace('<td>', '').replace('</td>', '')
            status = str(cells[1]).replace('<td>', '').replace('</td>', '')  
            
            _name = name.lower().replace(' ','')
            for k in keyword_list: 
                if k in _name: 
                    output.append('*%s* : %s' % (name, status)) 
        return '\n\n'.join(output)
    
    def parse_keywords(self):
        kwds = str(self.kwd_input.value).lower().replace(' ','').split(',')  
        return kwds


def main():
    return rumorScrape()
