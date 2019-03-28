import json
import urllib.request

from bs4 import BeautifulSoup

# url = 'http://nbviewer.jupyter.org/url/jakevdp.github.com/downloads/notebooks/XKCD_plots.ipynb'
# url = 'https://relate.cs.illinois.edu/course/cs450-s16/file-version/dc2f5b2a039e3a7b3014258f063a7faa2296ee1f/demos/upload/09-initial-value-problems/Forward%20Euler%20stability.html'

# response = urllib.request.urlopen(url)
#  for local html file
response = open(
    "/Users/tp5/Desktop/Masters_Resources/teaching/ME498_CMO/lectures/05_timeintegration/code/andreas_code/stiffness.html"
)
text = response.read()

soup = BeautifulSoup(text, 'lxml')
# see some of the html
print(soup.div)
dictionary = {'nbformat': 4, 'nbformat_minor': 1, 'cells': [], 'metadata': {}}
for d in soup.findAll("div"):
    if 'class' in d.attrs.keys():
        for clas in d.attrs["class"]:
            if clas in ["text_cell_render", "input_area"]:
                # code cell
                if clas == "input_area":
                    cell = {}
                    cell['metadata'] = {}
                    cell['outputs'] = []
                    cell['source'] = [d.get_text()]
                    cell['execution_count'] = None
                    cell['cell_type'] = 'code'
                    dictionary['cells'].append(cell)

                else:
                    cell = {}
                    cell['metadata'] = {}

                    cell['source'] = [d.decode_contents()]
                    cell['cell_type'] = 'markdown'
                    dictionary['cells'].append(cell)
open('notebook.ipynb', 'w').write(json.dumps(dictionary))
