from requests import post, put
from dotenv import load_dotenv # type: ignore
from os import getenv
import parsear_reporte as pr
from enviar_reporte import generar_body_headers

def autenticar_df(url:str,id:str,token:str):
    body = {
  "IdCliente": id,
  "JWToken": token
}
    response = post(url,json=body)
    return response.status_code

def main():
    load_dotenv("local.env")
    
    base_url = str(getenv("URL_API_DF"))
    id_cliente = str(getenv("ID_CLIENTE_API_DF"))
    token = str(getenv("TOKEN_API_DF"))
    auth_url = base_url+"/Autenticar"
    
    #autenticar_df(auth_url,id_cliente,token)
    asd = open("hola.txt","w")
    datos = pr.procesar()
    for i in range(len(datos)):
        url, body,headers = generar_body_headers(datos,i)
        
        #print(body)
        put(url,json=body,headers=headers)

if __name__=="__main__":
    main()