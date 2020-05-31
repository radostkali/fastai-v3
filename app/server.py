import os
import sys
import uvicorn
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

export_file_url = 'https://www.dropbox.com/s/6bgq8t6yextloqp/export.pkl?raw=1'
export_file_name = 'export.pkl'

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dist = os.path.join(path, 'dist')

app = Starlette(debug=True)
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory=os.path.join(dist, 'static')))


def fake_predict(image):
    from random import randint
    return bool(randint(0, 1))


@app.route('/')
async def homepage(request):
    path_to_html = os.path.join(dist, 'index.html')
    with open(path_to_html, 'r') as html:
        html_content = html.read()
    return HTMLResponse(html_content)


@app.route('/analyze', methods=['POST'])
async def analyze(request):
    img_data = await request.form()
    img_bytes = await (img_data['file'].read())
    img = BytesIO(img_bytes)
    prediction = fake_predict(img)
    return JSONResponse({'result': prediction})


if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")
