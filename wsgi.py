import sys

# Add your project directory to the Python path
path = '/home/your_username/ClickNBuild_Project'
if path not in sys.path:
    sys.path.append(path)

from app import create_app
application = create_app() 