import os
import pandas as pd
import string

class CriarTXTReivindicacoes:
    def __init__(self, input_csv_path, output_folder):
        self.input_csv_path = input_csv_path
        self.output_folder = output_folder

    def limpar_nome(self, nome_artigo):
        # Remove caracteres especiais e pontuações do nome do artigo
        allowed_chars = string.ascii_letters + string.digits + ' '
        cleaned_name = ''.join(char if char in allowed_chars else '_' for char in nome_artigo)
        return cleaned_name.strip()

    def criar_txt(self):
        # Criar o diretório de saída se não existir
        os.makedirs(self.output_folder, exist_ok=True)

        # Ler o CSV usando o pandas
        df = pd.read_csv(self.input_csv_path)

        # Iterar sobre as linhas do DataFrame
        for index, row in df.iterrows():
            nome_artigo = row['Nome']
            reivindicacoes = row['Descrição'].split('\n')

            # Limpar o nome do artigo para uso como nome de arquivo
            txt_filename = f"{self.limpar_nome(nome_artigo)}.txt"
            txt_path = os.path.join(self.output_folder, txt_filename)

            # Escrever as reivindicações em um arquivo .txt
            with open(txt_path, 'w', encoding='utf-8') as txtfile:
                for reivindicacao in reivindicacoes:
                    txtfile.write(reivindicacao + '\n')

# Exemplo de uso
input_csv_path = 'formulações+tópicas+anti-inflamatórias_artigos_filtrados.csv'
output_folder = 'reivindicacoes_txt'

criador_txt = CriarTXTReivindicacoes(input_csv_path, output_folder)
criador_txt.criar_txt()
