#!/bin/python3
"""
    jonatasrenan@dcc.ufmg.br
"""
from mascavo import file, csv, link, pdf, parallel


"""
1) O primeiro passo é fazer a coleta das informações das atas no site e, então,
salva-las no arquivo atas.csv;
2) Numa eventual segunda execução, caso o arquivo atas.csv já exista, deve-se 
pular a etapa de coleta e utilizar os dados de atas.csv;
3) Cada linha do arquivo atas.csv terá uma estrutura a seguir:
  {
      'tipo': tipo da ata (Comissão ou conselho relacionado);
      'ano': ano da ata;
      'ata': nome da ata;
      'url': url do arquivo pdf referente a ata;
  }
"""
atas = []
if file.exists('atas.csv'):
    atas = csv.read('atas.csv')
else:
    url_inicial = 'http://www.usp.br/secretaria/?p=3369'
    seletor_de_tipos = '.post > div.entry-content.article > ul > li > a'
    seletor_de_anos = '.page > div > ul > li > a'
    seletor_de_atas = '.page > div > p > a'

    tabela = []
    tipos = link.elements(url_inicial, seletor_de_tipos)
    for tipo in tipos:
        anos = link.elements(tipo['href'], seletor_de_anos)
        for ano in anos:
            atas = link.elements(ano['href'], seletor_de_atas)
            for ata in atas:
                linha = {'tipo': tipo['text'],
                         'ano': ano['text'],
                         'ata': ata['text'],
                         'url': ata['href']}
                tabela += [linha]
    csv.write(tabela, 'atas.csv')


"""
    Com os dados dos sites salvos em atas.csv, baixar os arquivos na pasta 
./downloads'
"""
arquivos_pdf = []
for ata in atas:
    url = ata['url']
    caminho_arquivo = link.download(url, './downloads')
    arquivos_pdf += [caminho_arquivo]


def processa(arquivo_pdf):
    """
        Dado um arquivo_pdf, converte-lo para txt e salvar na pasta ./textos/
    :param arquivo_pdf: caminho do arquivo pdf.
    :return: Nenhum retorno
    """
    arquivo, extension = file.file_and_extension(arquivo_pdf)
    new_extension = '.txt'
    pasta = './textos/'
    arquivo_txt = pasta + arquivo + new_extension
    print(arquivo_txt)
    pdf.to_txt(arquivo_pdf, arquivo_txt)


"""
        Com os arquivos já baixados, convertê-los para texto e salvar na pasta 
    ./textos:
        Como esse processamento é demorado, iremos executar em paralelo. Para
    isto, Foi utilizado o método pmap que aplica a a função processa() em cada 
    um dos itens da lista arquivos_pdf usando todos os núcleos do processador.
"""
parallel.pmap(processa, arquivos_pdf)
