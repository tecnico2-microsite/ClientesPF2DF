import parsear_reporte as pr
from datetime import date
from dotenv import load_dotenv
from os import getenv

load_dotenv("../local.env")
def generar_body_headers(datos:list,index:int):
    dato = datos[index][list(datos[index])[0]]
    body= {
  "Codigo": f"PF{dato['dni']}",
  "CUIT": dato["cuil"],
  "TipoDocumento": "05",
  "NroDocumento": dato["dni"],
  "PrimerNombre": dato["nombre"],
  "EMail": dato["email"],
  "Observacion": f'Cliente PE. Estado: {dato["estado"]}. Creado: {dato["fecha_alta"]}. Actualizado al día {str(date.today())}',
  "Telefono": dato["telefono"],
    }
    
    headers={
    "IdCliente":getenv("ID_CLIENTE_API_DF"),
    "Authorization":getenv("TOKEN_API_DF"),
    "BaseDeDatos":getenv("DATABASE"),
    "id":f"PF{dato['dni']}",
  }
    
    return body, headers





if __name__=="__main__":
  datos = pr.procesar()
  for i in range(len(datos)):
    body,headers = generar_body_headers(datos,i)
    print(body)
