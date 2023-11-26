import json

def manage_response(response:object):

    informe = response['Informes']['Informe']

    if informe['@respuesta'] == "13":
        return {
                'success': True,
                'data': json.loads(response)
            }
    else:
        return {
                'success': False,
                'data': json.loads(response)
            }