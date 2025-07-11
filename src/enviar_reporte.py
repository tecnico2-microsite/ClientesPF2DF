import parsear_reporte as pr
from datetime import date
from dotenv import load_dotenv
from os import getenv

load_dotenv("local.env")
def generar_body_headers(datos:list,index:int):
    dato = datos[index][list(datos[index])[0]]
    body= {
  "Codigo": dato['dni'],
  "CUIT": dato["cuil"],
  "TipoDocumento": "05",
  "NroDocumento": dato["dni"],
  "PrimerNombre": dato["nombre"],
  "EMail": dato["email"],
  "Observacion": f'Cliente PE. Estado: {dato["estado"]}. Creado: {dato["fecha_alta"]}. Actualizado al día {str(date.today())}',
  "Telefono": dato["telefono"],
  "CategCli":"PF"
    }
    
    headers={
    "IdCliente":str(getenv("ID_CLIENTE_API_DF")),
    "Authorization":str(getenv("TOKEN_API_DF")),
    "BaseDeDatos":str(getenv("DATABASE")),
    "id":str(dato['dni']),
    }
    url = str(getenv("URL_API_DF"))+"/Cliente/"+dato['dni']
    body = str(body).replace("'",'"')
    return url, body, headers





if __name__=="__main__":
  datos = pr.procesar()
  for i in range(len(datos)):
    url, body,headers = generar_body_headers(datos,i)
    print(body)
