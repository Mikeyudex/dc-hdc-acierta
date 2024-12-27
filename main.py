import xmltodict
from zeep import Client
from zeep import xsd, helpers
from zeep.wsse.signature import Signature
from zeep.wsse.username import UsernameToken
from zeep.transports import Transport
from requests import Session
from configs import CONFIGWS, ENV_SERVICE
 
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

    if ENV_SERVICE == 'DEV':
        USUARIO_OKTA = CONFIGWS['USUARIO_OKTA_DEV']
        CLAVE_OKTA = CONFIGWS['CLAVE_OKTA_DEV']
        URL_WS_ACIERTA = CONFIGWS['URL_SERVICE_ACIERTA_DEV']
        WS_CLAVE = CONFIGWS['WS_CLAVE_DEV']
        WS_USUARIO = CONFIGWS['WS_USUARIO_DEV']
    elif ENV_SERVICE == 'PROD':
        USUARIO_OKTA = CONFIGWS['USUARIO_OKTA_PROD']
        CLAVE_OKTA = CONFIGWS['CLAVE_OKTA_PROD']
        URL_WS_ACIERTA = CONFIGWS['URL_SERVICE_ACIERTA_PROD']
        WS_CLAVE = CONFIGWS['WS_CLAVE_PROD']
        WS_USUARIO = CONFIGWS['WS_USUARIO_PROD']

    session = Session()
    # Parametros conexion Keystore en extension .pem
    session.cert = './certs/2025/keypair_2025.pem'

    # Clave privada del ertificado y el certificado SSL en archivos independiente
    private_key_filename = './certs/2025/private.key.txt'
    public_key_filename = './certs/2025/www_galilea_co.txt'


    # usuario OKTA sin dominio y contraseña
    okta_user = UsernameToken(username=USUARIO_OKTA, password=CLAVE_OKTA)

    # Parametros Firma
    signature = Signature(private_key_filename, public_key_filename)
    transport = Transport(session=session)
    URL = URL_WS_ACIERTA

    ws_clave = WS_CLAVE
    ws_usuario = WS_USUARIO

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
        """ response_service = json.dumps(
            response_service, ensure_ascii=False, indent=4) """
        #print('Consulta OK - JSON\n', response_service)
        return {"success": True, "data": response_service}
        
    except Exception as e:
        print(e)
        return {
            'success': False,
            'data': [],
            'error': e
        }
