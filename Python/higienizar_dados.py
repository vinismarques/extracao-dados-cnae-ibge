import pandas as pd
import re


def limpar_texto(x):
    return x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower()


def processar(endereco_arquivo):

    # Lê planilha Excel
    xl = pd.ExcelFile(endereco_arquivo)
    df = xl.parse("Sheet1")

    # Remove acentuação e transforma texto em minúsculo
    cols = df.select_dtypes(include=[object]).columns       # Obtém array com nome das colunas presentes no dataframe.
    df[cols] = df[cols].apply(limpar_texto)                 # Usa função para processar a série inteira de cada uma das colunas. Poderia ser uma função lambda como a usada abaixo.

    # Remove não-dígitos das colunas de códigos especificadas
    regex = re.compile(r"[^\d]")                                                                # Para maior performance, compila regex que dá match em tudo que não for dígito.
    cols_codigos = ['Código Divisão', 'Código Grupo', 'Código Classe', 'Código Subclasse']      # Define array com nome das colunas de códigos.
    df[cols_codigos] = df[cols_codigos].apply(lambda x: x.astype(str).str.replace(regex, ""))   # Converte série para tipo string e depois remove caracteres diferentes de dígitos.

    # Escreve o dataframe de volta no arquivo Excel (sobrescreve)
    df.to_excel(endereco_arquivo, index=False)

