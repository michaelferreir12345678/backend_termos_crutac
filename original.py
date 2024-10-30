import pandas as pd
from reportlab.lib.pagesizes import A4, A3
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_JUSTIFY


def desenhar_titulo_com_fundo(c, x, y, texto):
    # Define a largura e altura do contêiner do título
    largura_cont = 510  
    altura_cont = 15
    # Desenha o retângulo cinza claro
    c.setFillColorRGB(0.9, 0.9, 0.9)  # Cor cinza claro
    c.rect(x, y - altura_cont + 11, largura_cont, altura_cont, fill=True, stroke=False)
    
    # Escreve o título sobre o contêiner
    c.setFillColorRGB(0, 0, 0)  # Cor do texto: preto
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x + 1, y, texto)
    
def adicionar_paragrafo(c, x, y, largura, texto, altura_pagina):
    styles = getSampleStyleSheet()
    estilo_paragrafo = ParagraphStyle(
        'CustomBodyText',
        parent=styles['BodyText'],
        fontSize=8,  
        leading=12, 
        alignment=TA_JUSTIFY 
    )
    paragrafo = Paragraph(texto, estilo_paragrafo)
    w, h = paragrafo.wrap(largura, y)
    if y - h < 50:
        c.showPage()
        y = altura_pagina - 50 
    paragrafo.drawOn(c, x, y - h)
    return y - h - 1 

def gerar_pdf_dados_aluno(dados):
    nome_arquivo = f"Termo_{dados['Nome'].replace(' ', '_')}.pdf"
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4

    # Título principal do documento
    c.setFont("Helvetica-Bold", 16)
    c.drawString(70, altura - 80, "TERMO DE COMPROMISSO DE ESTÁGIO OBRIGATÓRIO")

    # Seções com contêineres de fundo cinza
    desenhar_titulo_com_fundo(c, 40, altura - 120, "Dados da Instituição de Ensino")
    c.setFont("Helvetica", 8)
    c.drawString(40, altura - 135, "Nome: Universidade Federal do Ceará – UFC            CNPJ: 07.272.636/0001-31")
    c.drawString(40, altura - 150, "Endereço: Av. da Universidade, 2853, Benfica, Fortaleza - CE            Fone/Fax: (85) 3366 7413 / 3366 7881")
    c.drawString(40, altura - 165, "Representante Legal: Reitor Custódio Luís Silva de Almeida   Coordenador Agência de Estágios: Profa. Maria Ozilea Bezerra Menezes")
    
    desenhar_titulo_com_fundo(c, 40, altura - 185, "Dados da Unidade Concedente")
    c.setFont("Helvetica", 8)
    c.drawString(40, altura - 200, "Razão Social: Prefeitura Municipal de Beberibe            CNPJ: 07.528.292/0001-89            Fone: (85) 3336-6050")
    c.drawString(40, altura - 215, "Endereço: Rua Padre Assis Portela – Centro   CEP: 62840-00            Cidade/UF: BEBERIBE-CE            Setor: Secretaria de Saúde")
    c.drawString(40, altura - 230, "Representante Legal (Prefeito): Michele Cariello de Sá Queiroz Rocha")

    desenhar_titulo_com_fundo(c, 40, altura - 250, "Dados do Aluno")
    c.setFont("Helvetica", 8)
    c.drawString(40, altura - 265, f"Nome: {dados['Nome']}                       Curso: ODONTOLOGIA                       Semestre: ")
    c.drawString(40, altura - 280, f"CPF: {dados['CPF']}                       Matrícula: {dados['Matricula']}                       Endereço: {dados['Endereco']}")
    c.drawString(40, altura - 295, f"Telefone: {dados['Telefone']}")

    desenhar_titulo_com_fundo(c, 40, altura - 330, "Dados do Professor Orientador")
    c.setFont("Helvetica", 8)
    c.drawString(40, altura - 345, "Nome: Ana Karine Macedo Teixeira                       SIAPE: 3513644                       Telefone: (85) 33668404")

    clausulas = [
        ("", "As partes firmam o presente Termo de Compromisso de Estágio Obrigatório, observando o disposto na Lei nº 11.788 de 25 de setembro de 2008, na Resolução no 23/CEPE de 30 de outubro 2009 e no Termo de Convênio já firmado entre a Unidade Concedente e a UFC em 09/06/2016, além das seguintes cláusulas: "),
        ("CLÁUSULA PRIMEIRA: ", "Através deste Termo, a UNIDADE CONCEDENTE se compromete a conceder experiência prática profissional, não remunerada, ao ESTAGIÁRIO previamente selecionado, e com frequência regular no curso de graduação em que está matriculado na UFC, em conformidade com o Art. 3º, I, da Lei nº 11.788 de 25/09/2008."),
        ("", "As partes firmam o presente Termo de Compromisso de Estágio Obrigatório, observando o disposto na Lei nº 11.788 de 25 de setembro de 2008, na Resolução no 23/CEPE de 40 de outubro 2009 e no Termo de Convênio já firmado entre a Unidade Concedente e a UFC em 09/06/2016, além das seguintes cláusulas:"),
        ("CLÁUSULA SEGUNDA: ", "O estágio tem como objetivo proporcionar ao estudante integração entre teoria e prática, a partir de situações reais e adequadas de trabalho, visando ao seu aprimoramento profissional e pessoal, e obedecerá ao seguinte Plano de Atividades, devendo tais atividades ser compatíveis com o currículo e com os horários escolares do ESTAGIÁRIO, conforme estabelecem o art. 7o, parágrafo único, o art. 3o, III, e o art. 10 da Lei nº 11.788 de 25/09/2008:\nPlano de Atividades:\n- Acompanhar atividades assistenciais, seja em atividades preventivas e curativas compatíveis com a realidade das demandas e recursos dos serviços de saúde do município, prioritariamente na Atenção Primária à Saúde;\n- Acompanhar atividades de saúde coletiva, seja em atividades de gestão, gerenciamento, epidemiologia e educação em saúde."),
        ("Plano de Atividades", ""),
        ("-", "Acompanhar atividades assistenciais, seja em atividades preventivas e curativas compatíveis com a realidade das demandas e recursos dos serviços de saúde do município, prioritariamente na Atenção Primária à Saúde;"),
        ("-", "Acompanhar atividades de saúde coletiva, seja em atividades de gestão, gerenciamento, epidemiologia e educação em saúde."),
        ("CLÁUSULA TERCEIRA: ", "Além das atividades previstas no plano, ficam definidas as seguintes características do estágio: "),
        ("a)", "O estágio terá início em 04/11/2024 e término em 29/11/2024;"),
        ("b)", "O estudante terá jornada diária de 8 horas, sendo de segunda a sexta-feira, perfazendo no máximo quarenta (40) horas semanais, respeitando o art. 10 da Lei nº 11.788 de 25/09/2008."),
        ("c)", "A carga horária do estágio será reduzida pelo menos à metade nos períodos de avaliação do ESTAGIÁRIO, para garantir o bom desempenho do estudante, nos termos do Art. 10, §2o, da Lei n° 11.788 de 25/09/2008;"),
        ("d)", "A UFC oferece seguro contra acidentes pessoais a todos os seus estudantes devidamente matriculados, também contemplando o ESTAGIÁRIO, parte deste Termo, durante a vigência do presente. Seguem as informações do seguro: "),
        ("", "Empresa Seguradora: MBM Seguradora S.A."),
        ("", "Apólice: 16.0982.55416.001"),
        ("", "Vigência: de 01/12/2023 até 01/12/2024"),
        ("", "Vigência: de 01/12/2023 até 01/12/2024"),
        ("", "Morte Acidental: R$ 10.000,00"),
        ("", "Invalidez Permanente: R$ 10.000,00"), 
        ("CLÁUSULA QUARTA:", "Compete ao ESTAGIÁRIO:"),
        ("a)", "Cumprir as normas internas da UNIDADE CONCEDENTE, especialmente as de orientação do plano de atividades constante neste Termo, devendo apresentar à UFC, em prazo não superior a 6 (seis) meses, o relatório das atividades desenvolvidas"),
        ("b)", "Seguir a orientação articulada entre os Supervisores de Estágio designados pela UNIDADE CONCEDENTE e pela UFC;"),
        ("c)", "Diante da impossibilidade de cumprir o estabelecido neste Termo, comunicar a circunstância à UNIDADE CONCEDENTE, ficando esclarecido, desde logo, que suas obrigações escolares e a pertinência das atividades à sua  qualificação profissional serão consideradas motivos justos;"),
        ("d)", "Em caso de desistência do Estágio, comunicar à Secretaria Municipal de Saúde com antecedência mínima de 05 (cinco) dias e entregar termo de rescisão contratual à UFC, no setor competente"), 
        ("CLÁUSULA QUINTA: ", "São motivos para a rescisão imediata deste Termo de Compromisso de Estágio a ocorrência das seguintes hipóteses: "),
        ("a) ", "Conclusão, trancamento ou abandono do Curso;"),
        ("b) ", "Transferência para Curso que não tenha relação com as atividades de estágio desenvolvidas na Empresa;"),
        ("c) ", "Descumprimento do convencionado no presente Termo;"),
        ("d) ", "Prática comprovada de conduta danosa, não estando o ESTAGIÁRIO isento de arcar com as perdas e os danos desta decorrente."),
        ("CLÁUSULA SEXTA: ", "O estágio não acarretará vínculo empregatício de qualquer natureza, conforme Art. 3º, caput e § 2º, e Art. 2° da Lei nº 11.788 de 25/09/2008."),
        ("CLÁUSULA SÉTIMA: ", "O descumprimento das condições estabelecidas neste Termo pela UNIDADE CONCEDENTE caracteriza vínculo de emprego com o ESTAGIÁRIO, para todos os fins da legislação trabalhista e previdenciária, conforme estabelece o art. 15 da Lei nº 11.788 de 25/09/2008."),
        ("CLÁUSULA OITAVA: ", "Qualquer alteração do estabelecido neste Termo será feita mediante Aditivo, com a anuência das partes envolvidas."),
        ("CLÁUSULA OITAVA: ", "Qualquer alteração do estabelecido neste Termo será feita mediante Aditivo, com a anuência das partes envolvidas."),
        ("", "E, por estarem devidamente cientes das condições aqui estipuladas, bem como das disposições legais vigentes sobre o assunto, firmam a UNIDADE CONCEDENTE e o ESTAGIÁRIO, com interveniência da UFC, o presente TERMO, em 03 (três) vias de igual teor e forma, para que este produza seus devidos efeitos legais."),
        ("", "DECLARO, serem exatas e verdadeiras as informações aqui prestadas, sob pena de responsabilidade administrativa, cível e penal."),
    ]

    altura_clausulas = altura - 355
    for titulo, texto in clausulas:
        c.setFont("Helvetica", 8)
        altura_clausulas = adicionar_paragrafo(c, 40, altura_clausulas, 510, f"{titulo} {texto}", altura)

    c.drawString(40, altura - 450, f"Fortaleza - CE, _____ de _______________________ de 2024.")
    c.line(40, altura - 500, 250, altura - 500)  # Linha para assinatura do aluno
    c.drawString(40, altura - 510, f"{dados['Nome']}")
    c.drawString(40, altura - 520, "Estagiário")
    c.line(300, altura - 500, 500, altura - 500)  # Linha para assinatura do representante do município
    c.drawString(300, altura - 510, "Representante do Município")
    
    c.line(40, altura - 560, 250, altura - 560)  # Linha para assinatura do aluno
    c.drawString(40, altura - 570, "Professor(a) Orientador(a) - UFC")
    c.line(300, altura - 560, 500, altura - 560)  # Linha para assinatura do representante do município
    c.drawString(300, altura - 570, "Coordenador(a) do Curso de Odontologia - UFC")
    
    c.line(40, altura - 620, 250, altura - 620)  # Linha para assinatura do aluno
    c.drawString(40, altura - 630, "José Roberto Pereira de Sousa")
    c.drawString(40, altura - 640, "Coordenador do CRUTAC - UFC")
    
    # Salva o PDF
    c.showPage()
    c.save()
    print(f"PDF gerado: {nome_arquivo}")

# Lê a planilha com os dados dos alunos
dados_alunos = pd.read_excel("dados_alunos.xlsx")

# Gera um PDF para cada aluno
for _, dados in dados_alunos.iterrows():
    gerar_pdf_dados_aluno(dados)
