import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Use port 5001 to avoid conflicts with Windows services that often use 5000
    app.run(debug=True, port=5001)
