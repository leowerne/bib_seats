#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import re
!pip install cssutils
import cssutils

url = 'https://www.ub.uni-heidelberg.de/raumres/?building=Altstadt'
response = requests.get(url)
html_content= response.content
soup = BeautifulSoup(html_content, 'html.parser')

#%% Step 2: Load and Parse the CSS


with open('css/bootstrap.min.css', 'r') as file:
    css_content = file.read()

css_parser = cssutils.CSSParser()
stylesheet = css_parser.parseString(css_content)

#%% Step 3: Define a Function to Extract CSS Rules
def get_css_rules(stylesheet):
    rules = {}
    for rule in stylesheet.cssRules:
        if rule.type == rule.STYLE_RULE:
            selector = rule.selectorText
            styles = {style.name: style.value for style in rule.style}
            rules[selector] = styles
    return rules

css_rules = get_css_rules(stylesheet)

#%% Step 4: Match CSS Rules to HTML Elements
def apply_css_to_elements(soup, css_rules):
    element_styles = {}
    for selector, styles in css_rules.items():
        elements = soup.select(selector)
        for element in elements:
            if element not in element_styles:
                element_styles[element] = {}
            element_styles[element].update(styles)
    return element_styles

element_styles = apply_css_to_elements(soup, css_rules)

#%% Step 5: Print Styles for Key Elements
def print_element_styles(element_styles):
    for element, styles in element_styles.items():
        print(f"Element: {element.name}, Classes: {element.get('class')}")
        for property, value in styles.items():
            print(f"  {property}: {value}")
        print()

print_element_styles(element_styles)
