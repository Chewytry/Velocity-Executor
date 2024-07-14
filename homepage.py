from h2o_wave import main, app, Q, ui, on, run_on, site
import asyncio
from h2ogpte import H2OGPTE
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from slides_generation import generate_slides
import base64
from service import download_presentation
import requests
from recommendations import recommendations

async def home(q: Q):
    backgroundpath='https://getwallpapers.com/wallpaper/full/4/5/b/151051.jpg'

    html = '''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @font-face {
            font-family: 'CustomFont';
            src: url('path_to_your_font_file.ttf') format('truetype');
        }
        h1 {
            font-family: 'CustomFont', sans-serif; 
            text-align: center;
        }
        p {
        text-align: center; /* Center align the paragraph */
        }
    </style>
    </head>
    <body>
    <h1>Welcome to Travel.AI</h1>
    <p>Your one-stop platform for all your travel recommendation needs! </p>
    </body>
    </html>
    '''

    q.page['background'] = ui.image_card(box='1 1 12 12', title='', path=backgroundpath)
    q.page['header'] = ui.header_card(box='1 1 12 1', title='Travel.AI', subtitle='Discover your next adventure with us!',
                                    image='https://www.creativefabrica.com/wp-content/uploads/2021/03/20/Travel-logo-design-Graphics-9786083-1-1-580x435.jpg', color='transparent')
    q.page['example'] = ui.frame_card(box='4 3 6 2', title=' ', content=html, )
    q.page['continuebutton'] = ui.form_card(box='6 8 2 1', items=[ui.text(content=f'[Click here for adventure :)](#recommendations)', size='xl'),])
    await q.page.save()


    