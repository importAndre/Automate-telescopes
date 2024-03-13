import requests
import json

# API DOCS: https://aa.usno.navy.mil/data/api

def get_objects_by_date_coor(date, latitude, longitude):
    '''
    almanac_data: Dados do almanaque para o corpo celeste.

    dec: Declinação em graus, que é a latitude celeste ou ângulo norte/sul em relação ao equador celeste.
    gha: Ângulo horário de Greenwich, que indica a localização do astro em relação ao meridiano de Greenwich.
    hc: Altura calculada, que é o ângulo acima do horizonte.
    zn: Azimute, que é a direção do astro em relação ao norte geográfico, medido em graus.

        altitude_corrections: Correções aplicadas à altitude observada.

    isCorrected: Indica se foram aplicadas correções.
    pa: Correção paraláctica.
    refr: Correção de refração atmosférica.
    sd: Diâmetro semimaior aparente do objeto.
    sum: Soma das correções.
    '''

    url = f'https://aa.usno.navy.mil/api/celnav?date={date}&time=16:11&coords={latitude},{longitude}'

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data")

def extract_objects(data):
    objects = []
    for item in data:
        objects.append(item['object'])
    return objects

def select_visible_objects(infos, az_min, az_max, alt_min, alt_max):
    visible_objects = []
    for item in infos:
        item_info = item['almanac_data']
        item_az = item_info.get('zn', 0)
        item_alt = item_info.get('hc', 0)

        if (item_az > az_min and item_az < az_max) and (item_alt > alt_min and item_alt < alt_max):
            visible_objects.append(item['object'])
    return visible_objects

def get_info_by_name(objects, name):
    for item in objects:
        if item['object'] == name:
            item_info = item['almanac_data']
            zn = item_info['zn']
            hc = item_info['hc']
            return zn, hc

def get_telescope_position(init):
    # develop this later
    return init

def move_telescope(init, final):
    az_init, alt_init = init
    az_dest, alt_dest = final

    if az_init > az_dest:
        az_final = az_init - az_dest
    else:
        az_final = az_dest - az_init
    if alt_init > alt_dest:
        alt_final = alt_init - alt_dest
    else:
        az_final = alt_dest - alt_init

    return az_final, alt_final
    


if __name__ == '__main__':
    # date and coordinates
    date = '2024-3-13'
    latitude = '-23.5489'
    longitude = '-46.6388'

    # field of view
    az_min = 100
    az_max = 350
    alt_min = 20
    alt_max = 90

    data = get_objects_by_date_coor(date=date, latitude=latitude, longitude=longitude)
    objects_info = data['properties']['data']
    # print(json.dumps(objects_info, indent=4))
    objects = extract_objects(objects_info)

    visible_objects = select_visible_objects(infos=objects_info, az_min=az_min, az_max=az_max, alt_max=alt_max, alt_min=alt_min)
    
    desire_object = 'Sun'
    sun_pos = get_info_by_name(objects_info, desire_object)
    print(sun_pos)
    desire_object = 'Moon'
    moon_pos = get_info_by_name(objects_info, desire_object)
    print(moon_pos)

    path = move_telescope(init=sun_pos, final=moon_pos)
    print(path)

