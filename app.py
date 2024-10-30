from flask import Flask, request, send_file, jsonify
import pandas as pd
import io
from zipfile import ZipFile
from termos_crutac import gerar_pdf_dados_aluno  
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.route('/upload', methods=['POST'])
def upload_planilha():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files['file']
    df = pd.read_excel(file)

    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, 'w') as zip_file:
        for _, row in df.iterrows():
            pdf_buffer = gerar_pdf_dados_aluno(row)
            filename = f"Termo_{row['Nome'].replace(' ', '_')}.pdf"
            zip_file.writestr(filename, pdf_buffer.getvalue())  

    zip_buffer.seek(0)
    return send_file(zip_buffer, as_attachment=True, download_name="termos_estagio.zip", mimetype="application/zip")

if __name__ == '__main__':
    app.run(debug=True)
