# -*- coding: utf-8 -*-
"""
    jonatasrenan@dcc.ufmg.br
"""

import lxml.html
import requests
import requests_cache
from lxml.cssselect import CSSSelector
from src.utils import flat, cria_csv


def pmap(f, iter):
    return list(map(f, iter))


def get(endereco, seletor):
    """
    Acessa o "endereço" utilizando o método GET
    filtra resposta utilizando um determinado "seletor" CSS
    :param endereco: endereço a ser acessado
    :param seletor: seletor aplicado na resposta da requisição
    :return: resultados encontrados
    """
    requests_cache.install_cache('cache')
    resposta = requests.post(endereco)
    conteudo = lxml.html.fromstring(resposta.content)
    return CSSSelector(seletor)(conteudo)


def coleta_site():
    print('Coleta os tipos de atas')
    tipos = obter_tipos()
    print('Coleta quais os anos por tipo de ata ')
    anos = flat(map(obter_anos, tipos))
    print('Coleta informações das atas do site')
    atas = flat(map(obter_atas, anos))
    print('salva dados encontrados no site')
    cria_csv(atas, 'atas.csv')


def obter_tipos():
    url_base = 'http://www.usp.br/secretaria/?p=3369'
    seletores = get(url_base, '.post > div.entry-content.article > ul > li > a')

    def proc(s):
        return {
            'tipo': s.text,
            'url': s.get('href')
        }

    return pmap(proc, seletores)


def obter_anos(tipo):
    seletores = get(tipo['url'], '.page > div > ul > li > a')

    def proc(s):
        return {
            'ano': s.text,
            'url': s.get('href'),
            'tipo': tipo['tipo']
        }

    return pmap(proc, seletores)


def obter_atas(ano):
    seletores = get(ano['url'], '.page > div > p > a')

    def proc(s):
        return {
            'ata': s.text,
            'url': s.get('href'),
            'tipo': ano['tipo'],
            'ano': ano['ano']
        }

    return pmap(proc, seletores)
