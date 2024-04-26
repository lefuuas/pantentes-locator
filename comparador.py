import csv
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

class FiltrarReivindicacoes:
    def __init__(self, input_csv_path, output_csv_path):
        self.input_csv_path = input_csv_path
        self.output_csv_path = output_csv_path
        nltk.download('stopwords')  # Baixar a lista de stopwords

    def remover_stopwords(self, texto):
        stopwords_portugues = set(stopwords.words('portuguese'))
        palavras = texto.split()
        palavras_filtradas = [palavra for palavra in palavras if palavra.lower() not in stopwords_portugues]
        texto_filtrado = ' '.join(palavras_filtradas)
        return texto_filtrado

    def calcular_similaridade(self, reivindicacao, primeira_reivindicacao):
        # Criar vetorizador TF-IDF
        vetorizador = TfidfVectorizer()

        # Calcular as características TF-IDF dos textos
        matriz_tfidf = vetorizador.fit_transform([reivindicacao, primeira_reivindicacao])

        # Calcular similaridade de cosseno entre os textos
        similaridade = (matriz_tfidf * matriz_tfidf.T).A[0, 1] * 100  # Convertendo para porcentagem
        return similaridade

    def filtrar_reivindicacoes(self):
        with open(self.input_csv_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames

            with open(self.output_csv_path, 'w', newline='', encoding='utf-8') as output_csvfile:
                writer = csv.DictWriter(output_csvfile, fieldnames=['Nome', 'Descrição'])
                writer.writeheader()
                
                # Obter a primeira linha do arquivo CSV (primeira reivindicação)
                primeira_reivindicacao = next(reader)['Descrição']
                
                for row in reader:
                    nome_artigo = row['Nome']
                    reivindicacao = row['Descrição']
                    
                    similaridade_minima = 80
                    similaridade = self.calcular_similaridade(reivindicacao, primeira_reivindicacao)
                    print(f"Similaridade entre '{nome_artigo}' e a primeira reivindicação (90): {similaridade}")
                    if similaridade >= similaridade_minima:
                        writer.writerow({'Nome': nome_artigo, 'Descrição': reivindicacao})

# Exemplo de uso
input_csv_path = 'formulações+tópicas+anti-inflamatórias_artigos.csv'
output_csv_path = 'formulações+tópicas+anti-inflamatórias_artigos_filtrados.csv'

filtrador = FiltrarReivindicacoes(input_csv_path, output_csv_path)
filtrador.filtrar_reivindicacoes()
