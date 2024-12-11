from flask import Flask, request, send_file, jsonify
import pandas as pd
import io
from zipfile import ZipFile
from termos_crutac import gerar_pdf_dados_aluno  
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app) 

@app.route('/nomes_alunos', methods=['POST'])
def nomes_alunos():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    
    file = request.files["file"]
    
    try:
        # Tente ler o arquivo Excel
        df = pd.read_excel(file)

        # Log das colunas para verificar a correspondência
        print(f"Colunas encontradas: {df.columns.tolist()}")  # Depuração das colunas

        # Verifique se a coluna 'Nome' está presente
        if "Nome" not in df.columns:
            return jsonify({"error": "A planilha enviada não contém a coluna 'Nome'"}), 400

        # Verifique se as outras colunas necessárias existem
        required_columns = ["CPF", "Matricula", "Endereco", "Cidade/UF", "Telefone"]
        for column in required_columns:
            if column not in df.columns:
                return jsonify({"error": f"A planilha enviada não contém a coluna '{column}'"}), 400
        
        # Processamento dos dados
        nomes = df["Nome"].dropna().tolist()
        cpf = df["CPF"].dropna().tolist()
        matricula = df["Matricula"].dropna().tolist()
        endereco = df["Endereco"].dropna().tolist()
        cidade = df["Cidade/UF"].dropna().tolist()
        telefone = df["Telefone"].dropna().tolist()

        # Retorne os dados processados
        return jsonify({
            "students": nomes,
            "cpf": cpf,
            "matricula": matricula,
            "endereco": endereco,
            "cidade": cidade,
            "telefone": telefone
        }), 200
    
    except Exception as e:
        # Log do erro para depuração
        print(f"Erro ao processar o arquivo: {str(e)}")
        return jsonify({"error": f"Ocorreu um erro ao processar o arquivo: {str(e)}"}), 500
    
@app.route('/generate', methods=['POST'])
def generate_terms():
    # Validação dos dados enviados
    try:
        # Obtendo os dados JSON enviados
        data = request.get_json()

        # Extraindo informações do corpo da requisição
        numero_apolice = data.get("policyNumber")
        vigencia_inicio = data.get("startDate")
        vigencia_fim = data.get("endDate")
        students = data.get("students")

        # Verificando se todos os dados necessários foram fornecidos
        if not all([numero_apolice, vigencia_inicio, vigencia_fim, students]):
            return jsonify({"error": "Dados adicionais incompletos"}), 400

        # Carregando o arquivo de unidades concedentes
        with open('unidades_concedentes.json', 'r', encoding='utf-8') as f:
            unidades_concedentes = json.load(f)

        # Processando os dados dos alunos
        alunos = []
        for student in students:
            nome = student.get("name")
            cpf = student.get("cpf")
            matricula = student.get("matricula")
            endereco = student.get("endereco")
            cidade = student.get("cidade")
            telefone = student.get("telefone")
            unidade_concedente_nome = student.get("unit")

            # Validando dados do aluno
            if not all([nome, cpf, matricula, endereco, cidade, telefone, unidade_concedente_nome]):
                return jsonify({"error": f"Dados incompletos para o aluno {nome}"}), 400

            # Buscando os dados da unidade concedente com base na identificação
            unidade_concedente = next((u for u in unidades_concedentes if u['identificacao'] == unidade_concedente_nome), None)
            
            if not unidade_concedente:
                return jsonify({"error": f"Unidade concedente não encontrada para {unidade_concedente_nome}"}), 400

            alunos.append({
                "nome": nome,
                "cpf": cpf,
                "matricula": matricula,
                "endereco": endereco,
                "cidade": cidade,
                "telefone": telefone,
                "unidade_concedente": unidade_concedente
            })

        # Gerando o arquivo ZIP com os termos
        zip_buffer = io.BytesIO()
        with ZipFile(zip_buffer, 'w') as zip_file:
            for aluno in alunos:
                # Gerando o PDF com os dados do aluno e os dados da unidade concedente
                pdf_buffer = gerar_pdf_dados_aluno(
                    aluno["nome"],
                    aluno["cpf"],
                    aluno["matricula"],
                    aluno["endereco"],
                    aluno["cidade"],
                    aluno["telefone"],
                    numero_apolice,
                    vigencia_inicio,
                    vigencia_fim,
                    aluno["unidade_concedente"]
                )

                # Nome do arquivo PDF com o nome do aluno
                filename = f"Termo_{aluno['nome'].replace(' ', '_')}.pdf"
                zip_file.writestr(filename, pdf_buffer.getvalue())

        # Preparando o arquivo zip para download
        zip_buffer.seek(0)
        return send_file(
            zip_buffer,
            as_attachment=True,
            download_name="termos_estagio.zip",
            mimetype="application/zip"
        )

    except Exception as e:
        # Caso ocorra algum erro no processo
        return jsonify({"error": f"Erro ao processar: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

