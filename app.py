from h2o_wave import main, app, Q

from homepage import home
from recommendations import recommendations

@app('/')
async def serve(q: Q):
    route = q.args['#']
    q.page.drop()
    if route == 'recommendations':
        await recommendations(q)
    else:
        await home(q)
