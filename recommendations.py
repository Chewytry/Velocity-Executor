from h2o_wave import main, app, Q, ui, site
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

async def recommendations(q: Q):
    load_dotenv()

    if not q.user.initialized:
        q.user.chat_session_id = os.getenv("CHAT_ID")
        q.user.client = H2OGPTE(
            address='https://h2ogpte.genai.h2o.ai',
            api_key=os.getenv("API_KEY")
        )
        q.user.collection_id = os.getenv("COLLECTION_ID")
        q.user.output_collection_id = os.getenv("OUTPUT_COLLECTION_ID")
        q.user.doc_id = ''
        q.user.initialized = True
        q.user.slides = None
        q.user.theme = None

    with open('themes/summer/summer-conclusion.png', 'rb') as img: 
        summerimage = base64.b64encode(img.read()).decode('utf-8')

    with open('themes/fall/fall-intro.png', 'rb') as img: 
        fallimage = base64.b64encode(img.read()).decode('utf-8')

    with open('themes/spring/spring-intro.png', 'rb') as img: 
        springimage = base64.b64encode(img.read()).decode('utf-8')

    with open('themes/winter/winter-intro.png', 'rb') as img: 
        winterimage = base64.b64encode(img.read()).decode('utf-8')
    

    backgroundpath='https://getwallpapers.com/wallpaper/full/4/5/b/151051.jpg'

    q.page['background'] = ui.image_card(box='1 1 12 12', title='', path=backgroundpath)
    q.page['header'] = ui.header_card(box='1 1 12 1', title='Travel.AI', subtitle='Discover your next adventure with us!',
                                    image='https://www.creativefabrica.com/wp-content/uploads/2021/03/20/Travel-logo-design-Graphics-9786083-1-1-580x435.jpg', color='transparent')
    q.page['prompt'] = ui.form_card(box='4 3 6 5', items=[
        ui.textbox(name='textbox', label='Questions?', placeholder='Example: Give me 3 countries to travel to in December', width='845px', required=True), 
        ui.text(content=" "),
        ui.text(content=' '),
        ui.text(content=' '),
        ui.choice_group(name='theme', label='Powerpoint Theme', required=True, choices=[
            ui.choice('Summer', 'Summer'), 
            ui.choice('Winter', 'Winter'), 
            ui.choice('Spring', 'Spring'), 
            ui.choice('Fall', 'Fall')
        ]),
        ui.text(content=" "),
        ui.button(name='preview', label='Slides Theme Preview?'),
        ui.text(content=' '),
        ui.text(content=' '),
        ui.text(content=' '),
        ui.button(name='submitbutton', label='Submit')
    ])

    if q.args.theme:
        if q.args.theme == 'Summer': 
            q.page['background']['path']=f'data:image/png;base64,{summerimage}'
        elif q.args.theme == 'Winter':
            q.page['background']['path']=f'data:image/png;base64,{winterimage}'
        elif q.args.theme == 'Fall':
            q.page['background']['path']=f'data:image/png;base64,{fallimage}'
        else:
            q.page['background']['path']=f'data:image/png;base64,{springimage}'

    if q.args.theme and q.args.textbox:
        q.user.theme = q.args.theme
        if q.args.submitbutton:
            prompt = ui.text(q.args.textbox).text.content

            content, title = parse_prompt(prompt, q.user.client, q.user.chat_session_id)
            q.user.slides = slide_processing(content, title, q.user.client, q.user.output_collection_id, q.user.theme)
            
            await asyncio.sleep(0)

            download_url = "http://localhost:5001/download_presentation/themed_presentation.pptx"
            
            q.page['download'] = ui.form_card(box='6 8 2 1', items=[
                ui.text(content=f'Successfully prepared slides for download. [Click here to download]( {download_url})'),
                ])
            
            await asyncio.sleep(0)
    if q.user.slides:
        q.page['meta'] = ui.meta_card(
            box='',
            notification_bar=ui.notification_bar(
                text='Successfully generated slides',
                type='success',
                position='top-right'
        ))

    await q.page.save()

def get_downloads_folder():
    """
    Returns the path to the user's Downloads folder.
    """
    home = Path.home()
    downloads_folder = home / 'Downloads'
    return str(downloads_folder)


def parse_prompt(prompt, client, chat_session_id):
    """
    Function to take in the prompt from the user, the client and chat_session_information and passes it to the H2O APIs to output the countries' information and the possible titles 
    """
    
    detail ="""Ensure the countries are from different continents, for each country give me 3 attractions each and a short write up for the country.
            Ensure that the countries are in itself quite popular, do not give countries that are largely unheard of.
            For each attraction give it to me in the format of: 1. Country (Continent) \n 
            * Attraction 1: {attraction name}: <description> \n 
            * Attraction 2: {attraction name}: <description> \n 
            * Attraction 3: {attraction name}: <description>"""
    
    title_prompt = """
    if I am creating a brochure based on countries to travel to, what is 1 formal and professional name I can give to the travel brochure to attract tourism, just give it to me in the response, no need for other comments or formatting for example, just respond: Tropical Treasures: Discover French Guiana, Suriname, and Guyana
    """

    with client.connect(chat_session_id) as session:
        reply = session.query(
            prompt + detail,
            timeout=60,
        )

        title = session.query(
            message='Based on this information:' + reply.content + title_prompt,
            timeout=60,
        )
    return reply.content, title.content

def slide_processing(content, title, client, output_collection_id, theme):
    """
    Function that takes in the content outputted from the pipeline to be used to process the slides.
    """
    file_name = 'themed_presentation.pptx'
    prs = generate_slides(content, theme, title)
    now = datetime.now()
    dt_string = now.strftime("%Y-%H-%M-%S")
    # with open(file_name, 'rb') as file:
        # upload_id = client.upload(f'{dt_string}.pptx', file=file)
    # client.ingest_uploads(collection_id=output_collection_id, upload_ids=[upload_id])
    # docs = client.list_recent_documents(offset=0, limit=1000)
    # for doc in docs:
    #     if doc.name == f'{dt_string}.pdf':
    return prs

def download_slides(presentation, title="Best Travel Guide"):
    """
    Function that 'downloads' the slides by copying the file to downloads.
    """
    timestamp = datetime.now()
    timestamp = timestamp.strftime("%Y %H-%M-%S")
    downloads_folder = get_downloads_folder()
    presentation.save(downloads_folder + f"\\{title}-{timestamp}.pptx")
    # client.download_document(downloads_folder, f'{title}-{timestamp}.pptx', doc_id)
    requests.get('http://localhost:5001/download_presentation/themed_presentation.pptx')
    return 200