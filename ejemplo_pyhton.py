
import xmltodict, json
from requests.except3
from zeep import Client
from zeep import xsd, helpers
from zeep.wsse.signature import Signature
from zeep.wsse.username import UsernameToken
from zeep.transports import Transport
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.plugins import HistoryPlugin
from lxml import etree
from zeep.exceptions import Fault

class CustomSignature(object):
    def __init__(self,wsse_list):
        self.wsse_list = wsse_list
        
    def apply(self, envelope, headers):
        for wsse in self.wsse_list:
            envelope, headers = wsse.apply(envelope, headers)
        return envelope, headers
    
    def verify(self, envelope):
        pass
        

session = Session()
#Parametros conexion Keystore en extension .pem
session.cert = '../demo_2021_sign.pem' 

#Clave privada del ertificado y el certificado SSL en archivos independiente
private_key_filename='../private_key_2021_sign.txt'
public_key_filename='../public_ssl_2021_sign.txt'

#usuario OKTA sin dominio y contraseña
okta_user = UsernameToken('2-XXXXXXXXX','xxxxxxx')

#Parametros Firma
signature = Signature(private_key_filename, public_key_filename)
transport = Transport(session= session)

URL='https://demo-servicesesb.datacredito.com.co:443/wss/dhws3/services/DHServicePlus?wsdl'

ws_clave='XXXXX'
ws_usuario='XXXXXXXXX'


client = Client(URL, wsse=CustomSignature([okta_user, signature]), transport= transport,)
client.service._binding_options["address"]=URL.replace('?wsdl','')
    
request_data={
       'clave':ws_clave,
        'identificacion':'52055212',
        'primerApellido':'rincon',
        'producto':'64',
        'tipoIdentificacion':'1',
        'usuario':ws_usuario,
        }

response_service= client.service.consultarHC2(solicitud=request_data)

print(response_service, '\n')
#CONVERSION XML A JSON
response_service= response_service.replace('&lt;','<')
response_service= helpers.serialize_object(response_service)
response_service= xmltodict.parse(response_service)
response_service= json.dumps(response_service, ensure_ascii=False,indent=4)
print('Consulta OK - JSON\n', response_service)
    
