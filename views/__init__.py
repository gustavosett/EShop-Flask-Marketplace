import os
import importlib
from pathlib import Path

pasta = Path(__file__).resolve().parent
blueprints = []


for diretorio, subpastas, arquivos in os.walk(pasta):
    for arquivo in arquivos:
        if not any(substring in arquivo for substring in [".pyc", "_"]):
            nome_modulo = os.path.splitext(arquivo)[0]
            modulo = importlib.import_module(f'.{nome_modulo}', package='views')
            try:
                blueprint = getattr(modulo, nome_modulo)
                blueprints.append(blueprint)
            except:
                print(f'Não foi possivel importar o módulo: "{modulo}"')
                pass
