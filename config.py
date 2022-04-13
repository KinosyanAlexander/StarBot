import os


BOT_TOKEN = os.getenv('BOT_TOKEN')
DATA_PATH = 'data'
DATABASE = os.path.join(DATA_PATH, 'Dictations.db')
TMP_DATA = os.path.join(DATA_PATH, 'users_data')

# webhook settings
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
SECRET_PATH = os.getenv('SECRET_PATH')
WEBHOOK_PATH = f'/webhook/{SECRET_PATH}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'  # or ip
WEBAPP_PORT = os.getenv('PORT', default=8000)
