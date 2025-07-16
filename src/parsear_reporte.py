import xlrd as x
import json
import obtener_reporte


def parsear_xls(name:str="Usuarios.xls"):
    sheet =  x.open_workbook(name).sheet_by_index(0)
    all_users=[]
    
    for i in range(3,sheet.nrows):
        if sheet.row(i)[3].value=="Empresa" or len(sheet.row(i)[7].value)>8:
            continue
        
        
        user = {str(i-2):{
            "empresa":sheet.row(i)[0].value,
            "email":sheet.row(i)[1].value,
            "nombre":sheet.row(i)[2].value,
            "tipo":sheet.row(i)[3].value,
            "telefono":sheet.row(i)[4].value,
            "dni":sheet.row(i)[7].value,
            "cuil":sheet.row(i)[8].value,
            "estado":sheet.row(i)[9].value,
            "fecha_alta":sheet.row(i)[10].value,
            "fecha_baja":sheet.row(i)[11].value,
            "fecha_reactivacion":sheet.row(i)[12].value
        }}
        
        all_users.append(user)
    return all_users
    


def generar_json(user_list:object):
    try:
        with open("users.json","x",encoding="utf-8") as newJson:
            newJson.write("[]")
            newJson.close()
        generar_json(user_list)
    except FileExistsError:

        with open("users.json","w",encoding="utf-8") as f:
            json.dump(user_list,f,indent=2,ensure_ascii=False)
            f.close()

def diferencias_a_cargar(archivo:list,parseado:list):
    """archivo: JSON parseado: XLS"""
    diferencias=[]
    
    cantidad_diferencias = len(parseado)-len(archivo)
    
    if cantidad_diferencias>0:
        for i in range(cantidad_diferencias):
            diferencias.append(parseado[i+len(archivo)])
            
    
    for i in range(min(len(parseado),len(archivo))):
        if parseado[i]!=archivo[i]:
            diferencias.append(parseado[i])
    
    return diferencias

def procesar():
    global archivo, parseado
    try:
        with open("users.json","x",encoding="utf-8") as newJson:
            newJson.write("[]")
            newJson.close()
        procesar()
    except:
        obtener_reporte.main()
        parseado = parsear_xls()
        file = open("users.json","r",encoding="utf-8")
        archivo = json.loads(file.read())
        file.close()
    
    return diferencias_a_cargar(archivo,parseado)
    
if __name__=="__main__":
    #generar_json(parsear_xls("Usuarios.xls"))
    #print(parsear_xls())
    parseado = parsear_xls()
    file = open("users.json","r",encoding="utf-8")
    archivo = json.loads(file.read())
    file.close()
    
    print(diferencias_a_cargar(archivo,parseado))