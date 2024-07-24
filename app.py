from flask import Flask, request, render_template, send_file, make_response
import requests
import os

app = Flask(__name__)

# Ganti dengan API key DocRaptor Anda
DOC_RAPTOR_API_KEY = 'mC5OrJ9rmtDrE-c3pOC6'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        pdf_name = request.form['pdf_name']
        
        if not pdf_name or any(c in pdf_name for c in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']):
            return "Invalid PDF name. Please avoid using special characters."

        pdf_path = os.path.join(os.getcwd(), f'{pdf_name}.pdf')

        try:
            response = requests.post(
                'https://docraptor.com/docs',
                auth=(DOC_RAPTOR_API_KEY, ''),
                json={
                    'document_url': url,
                    'name': pdf_path,
                    'test': True
                },
                headers={'Content-Type': 'application/json'},
                stream=True
            )

            if response.status_code == 200:
                # Menulis PDF ke file sistem
                with open(pdf_path, 'wb') as f:
                    f.write(response.content)

                # Mengirimkan file untuk diunduh oleh pengguna
                resp = make_response(send_file(pdf_path, as_attachment=True))
                resp.headers["Content-Disposition"] = f"attachment; filename={pdf_name}.pdf"
                return resp
            else:
                return f"An error occurred: {response.text}"
        except Exception as e:
            return f"An error occurred: {e}"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
