"""
Web Server Gateway Interface: initializes the app by calling create_app() from __init__.py
"""

from maintenance_app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
