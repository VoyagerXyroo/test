from flask import Flask, request, render_template, send_file
import requests
from io import BytesIO

app = Flask(__name__)

DOC_RAPTOR_API_KEY = 'mC5OrJ9rmtDrE-c3pOC6'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        pdf_name = request.form['pdf_name']

        if not pdf_name or any(c in pdf_name for c in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']):
            return "Invalid PDF name. Please avoid using special characters."

        try:
            response = requests.post(
                'https://docraptor.com/docs',
                auth=(DOC_RAPTOR_API_KEY, ''),
                json={'document_url': url, 'test': True},
                headers={'Content-Type': 'application/json'},
                stream=True
            )
            
            if response.status_code == 200:
                pdf_file = BytesIO(response.content)
                return send_file(pdf_file, as_attachment=True, download_name=f'{pdf_name}.pdf')
            else:
                return f"An error occurred: {response.text}"
        except Exception as e:
            return f"An error occurred: {e}"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
