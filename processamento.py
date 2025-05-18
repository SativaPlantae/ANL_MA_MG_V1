import geopandas as gpd
from shapely.geometry import Point
import os
import zipfile

def analisar_coordenada(x, y, pasta_camadas='camadas'):
    ponto = Point(x, y)
    resultado = {
        'Grupo': 'Não classificado',
        'Status': '',
        'campos': {
            'dm': 'Não',
            'restricoes': 'Não',
            'licenca': 'Não',
            'tapm': 'Não',
            'sensibilidade': 'Não'
        }
    }

    zip_nomes = {
        'dm': 'dm.zip',
        'restricoes': 'restricao.zip',
        'licenca': 'licenca.zip',
        'tapm': 'tapm.zip',
        'sensibilidade': 'sensibilidade.zip'
    }

    for campo, zip_nome in zip_nomes.items():
        pasta = os.path.join(pasta_camadas, campo)
        zip_path = os.path.join(pasta, zip_nome)

        if not os.path.exists(zip_path):
            continue

        temp_folder = os.path.join(pasta_camadas, f"temp_{campo}")
        os.makedirs(temp_folder, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_folder)

        shp_files = [f for f in os.listdir(temp_folder) if f.endswith('.shp')]
        if not shp_files:
            continue

        shp_path = os.path.join(temp_folder, shp_files[0])
        gdf = gpd.read_file(shp_path).to_crs(epsg=31983)

        if gdf.contains(ponto).any():
            resultado['campos'][campo] = 'Sim'

    campos = resultado['campos']

    dm = campos['dm'] == 'Sim'
    dm_nao = campos['dm'] == 'Não'
    restricoes = campos['restricoes'] == 'Sim'
    restricoes_nao = campos['restricoes'] == 'Não'
    licenca = campos['licenca'] == 'Sim'
    tapm = campos['tapm'] == 'Sim'
    tapm_nao = campos['tapm'] == 'Não'
    sensibilidade = campos['sensibilidade'] == 'Sim'
    sensibilidade_nao = campos['sensibilidade'] == 'Não'

    if dm_nao or restricoes:
        resultado['Grupo'] = 'Bloqueado'
        resultado['Status'] = 'Restrição fatal'

    elif dm and restricoes_nao:
        if tapm or licenca:
            resultado['Grupo'] = 'Antropizado'
            resultado['Status'] = 'Imediato'
        elif tapm_nao:
            resultado['Grupo'] = 'Antropizado'
            resultado['Status'] = 'TAPM'
        elif sensibilidade_nao:
            resultado['Grupo'] = 'Licenciamento'
            resultado['Status'] = 'Sem restrição'
        elif sensibilidade:
            resultado['Grupo'] = 'Licenciamento'
            resultado['Status'] = 'Restrição não fatal'
        else:
            resultado['Grupo'] = 'Licenciamento'
            resultado['Status'] = 'Próximas fases'

    return resultado
