from requests import post, put
from sys import exit
from dotenv import load_dotenv
from os import getenv
import parsear_reporte as pr
from enviar_reporte import generar_body_headers
from datetime import datetime
from parsear_reporte import generar_json, parsear_xls
#import ctypes
def autenticar_df(url:str,id:str,token:str):
    body = {
  "IdCliente": id,
  "JWToken": token
}
    response = post(url,json=body)
    return response

def main():
    try:
        log = open("log.err","x")
        log.close()
        main()
    except FileExistsError:
            
        log = open("log.err","a")
        try:
            load_dotenv("local.env")
            
            base_url = str(getenv("URL_API_DF"))
            id_cliente = str(getenv("ID_CLIENTE_API_DF"))
            token = str(getenv("TOKEN_API_DF"))
            auth_url = base_url+"/Autenticar"
            res = autenticar_df(auth_url,id_cliente,token)
            print("Autenticación: ", res.status_code)
        except Exception as e:
            #ctypes.windll.user32.MessageBoxW(0,"Ocurrió un error al sincronizar clientes de Peso Fuerte. \r\nComunicarse con Microsite Argentina","Error",0)
            print("Ocurrió un error")
            log.write("\r\n")
            log.write(f"{datetime.now()}")
            log.write(str(e))
            exit(1)
            
        datos = pr.procesar()
        for i in range(len(datos)):
            try:
                url, body,headers = generar_body_headers(datos,i)
                response = put(url,json=body,headers=headers)
                print(response.status_code)
                print(response.reason)
                if response.status_code!=200 and response.status_code!=201:
                    print("Ocurrió un error")
                    #ctypes.windll.user32.MessageBoxW(0,"Ocurrió un error al sincronizar clientes de Peso Fuerte. \r\nComunicarse con Microsite Argentina","Error",0)
                    log.write("\r\n")
                    log.write(f"{datetime.now()}")
                    log.write(response.status_code, response.reason)
                    log.write(response.headers)
                    log.write(response.content)
                    exit(1)
                    

            except Exception as e:
                print("Ocurrió un error")
                #ctypes.windll.user32.MessageBoxW(0,"Ocurrió un error al sincronizar clientes de Peso Fuerte. \r\nComunicarse con Microsite Argentina","Error",0)
                log.write("\r\n")
                log.write(f"{datetime.now()}")
                log.write(str(e))
                exit(1)
                
            #print(headers)
        log.close()
        generar_json(parsear_xls())
if __name__=="__main__":
    main()
