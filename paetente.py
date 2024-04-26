from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

class GooglePatentsScraper:
    def __init__(self, termo):
        self.termo = termo
        self.base_url = f'https://patents.google.com/?q=({termo})&oq={termo}&page='
        self.driver = webdriver.Chrome()

    def extrair_e_salvar_artigos(self):
        try:
            page_number = 1
            while True:
                url = f'{self.base_url}{page_number}'
                self.navegar_para_pagina(url)
                self.coletar_e_salvar_artigos()

                # Verificar se há próxima página
                if not self.tem_proxima_pagina():
                    break

                page_number += 1

        except Exception as e:
            print(f'Erro ao extrair e salvar artigos: {e}')

        finally:
            self.driver.quit()

    def navegar_para_pagina(self, url):
        self.driver.get(url)

    def coletar_e_salvar_artigos(self):
        # Abrir o arquivo CSV para escrita
        with open(f'{self.termo}_artigos.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Nome', 'Descrição']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Verificar se o arquivo está vazio para escrever o cabeçalho
            if csvfile.tell() == 0:
                writer.writeheader()

            # Aguardar até que os resultados carreguem
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'article.result')))

            # Encontrar todos os artigos
            artigos = self.driver.find_elements(By.CSS_SELECTOR, 'article.result')

            for index in range(len(artigos)):
                # Atualizar a lista de artigos para evitar elementos "stale"
                artigos = self.driver.find_elements(By.CSS_SELECTOR, 'article.result')
                nome_artigo = artigos[index].find_element(By.CSS_SELECTOR, 'h3').text
                # Obter o link do artigo
                link_artigo = artigos[index].find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                artigos[index].find_element(By.CSS_SELECTOR, 'a').click()

                try:
                    # Aguardar até que o título do artigo seja carregado

                    # Aguardar até que a descrição do artigo seja carregada
                    texto_artigo = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'claims'))).text

                    # Escrever os dados no arquivo CSV
                    writer.writerow({'Nome': f'{nome_artigo}', 'Descrição': f"{texto_artigo}"})

                    print(f'Dados salvos para o artigo: {nome_artigo}')

                except Exception as e:
                    print(f'Erro ao processar artigo: {e}')

                finally:
                    # Voltar para a página de resultados de pesquisa
                    self.driver.execute_script("window.history.go(-1)")  # Voltar para a página anterior
                    # Aguardar até que os resultados carreguem novamente (após voltar)
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'article.result')))


    def tem_proxima_pagina(self):
        try:
            next_button = self.driver.find_element(By.ID, 'icon')
            next_button.click()  # Clicar no botão de próxima página
            return True
        except Exception:
            return False  # Retornar False se o botão de próxima página não for encontrado


# Exemplo de uso
termo_busca = 'formulações+tópicas+anti-inflamatórias'
scraper = GooglePatentsScraper(termo_busca)
scraper.extrair_e_salvar_artigos()






