#!/bin/python3
# -*- coding: utf-8 -*-
"""
    Script principal

    jonatasrenan@dcc.ufmg.br
"""
from src.web import coleta_site
from src.arquivos import download, pdf2txt
from src.utils import le_csv, pmap, tmap
import os

# para refazer a coleta do site, delete o arquivo atas.csv
atas = le_csv('atas.csv') if os.path.isfile('atas.csv') else coleta_site()
# Download das atas
arquivos = tmap(download, atas)
# Converte documentos de PDF para texto
arquivos = tmap(pdf2txt, arquivos)

