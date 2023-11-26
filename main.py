import xmltodict
import json
from zeep import Client
from zeep import xsd, helpers
from zeep.wsse.signature import Signature
from zeep.wsse.username import UsernameToken
from zeep.transports import Transport
from requests import Session
from manageResponse import manage_response
 
class CustomSignature(object):
    def __init__(self, wsse_list):
        self.wsse_list = wsse_list

    def apply(self, envelope, headers):
        for wsse in self.wsse_list:
            envelope, headers = wsse.apply(envelope, headers)
        return envelope, headers

    def verify(self, envelope):
        pass

def getDataExperian(document:str = '74244054', lastname:str='GUARIN'):

    session = Session()
    # Parametros conexion Keystore en extension .pem
    session.cert = './certs/galilea_co.pem'

    # Clave privada del ertificado y el certificado SSL en archivos independiente
    private_key_filename = './certs/privkey.txt'
    public_key_filename = './certs/galilea_public.crt'


    # usuario OKTA sin dominio y contraseña
    okta_user = UsernameToken(username='2-901582748', password='AtlasM#2022')

    # Parametros Firma
    signature = Signature(private_key_filename, public_key_filename)
    transport = Transport(session=session)
    URL = 'https://demo-servicesesb.datacredito.com.co/wss/dhws3/services/DHServicePlus?wsdl'

    ws_clave = '57PFH'
    ws_usuario = '901582748'

    client = Client(URL, wsse=CustomSignature([okta_user, signature]), transport=transport,)
    client.service._binding_options["address"] = URL.replace('?wsdl', '')

    request_data = {
        'clave': ws_clave,
        'identificacion': document,
        'primerApellido': lastname,
        'producto': '64',
        'tipoIdentificacion': '1',
        'usuario': ws_usuario,
    }

    try:
        response_service = client.service.consultarHC2(solicitud=request_data)

        #print(response_service, '\n')
        # CONVERSION XML A JSON
        response_service = response_service.replace('&lt;', '<')
        response_service = helpers.serialize_object(response_service)
        response_service = xmltodict.parse(response_service)
        response_service = json.dumps(
            response_service, ensure_ascii=False, indent=4)
        #print('Consulta OK - JSON\n', response_service)
        return manage_response(response_service)
        
    except Exception as e:
        print(e)
        return {
            'success': False,
            'data': [],
            'error': e
        }
