import sys
import site
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

site_paths = [
    r'C:\Users\alfif\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages',
]
for p in site_paths:
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)
        site.addsitedir(p)

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
