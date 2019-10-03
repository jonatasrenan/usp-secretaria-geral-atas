# -*- coding: utf-8 -*-
"""
    jonatasrenan@dcc.ufmg.br
"""


def download(arquivo):
    """
    Baixa o arquivo na subpasta downloads
    :param arquivo: dicionario contendo os dados do arquivo
    :return: dados do arquivo atualizado
    """
    import os
    import urllib
    from requests.utils import requote_uri
    url = arquivo['url']
    name = url.split('/')[-1]
    path = os.path.join('./downloads', name)
    url = requote_uri(url)
    arquivo['filepath'] = path
    if not os.path.isfile(path):
        try:
            urllib.request.urlretrieve(url, path)
            print('Baixado (%s): %s' % (arquivo['url'], arquivo['filepath']))
        except urllib.error.HTTPError as e:
            print("%s %s" % (e, url))
            arquivo['filepath'] = None
    return arquivo


def pdf2txt(arquivo):
    """
    Converte arquivo baixado para formato texto na subpasta htmls
    :param arquivo:
    :return: dados do arquivo atualizado
    """
    import os
    import subprocess
    arquivo['pdf'] = arquivo['filepath']
    del arquivo['filepath']
    if not arquivo['pdf']:
        return arquivo
    arquivo['html'] = arquivo['pdf'].replace('/downloads/', '/htmls/').replace('.pdf', '.html')
    if not os.path.isfile(arquivo['html']):
        command = ["pdf2txt.py", "-W0", "-L1", "-t", "text", "-o", arquivo['html'], arquivo['pdf']]
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        with open(arquivo['html'] + '.out', 'w') as file:
            file.write(str(proc.communicate()[0]))
            file.close()
        with open(arquivo['html'] + '.err', 'w') as file:
            file.write(str(proc.communicate()[1]))
            file.close()
        print('Convertido pdf2txt: %s para %s' % (arquivo['html'], arquivo['pdf']))
    return arquivo
