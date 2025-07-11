import requests, re
from os import getenv
from dotenv import load_dotenv # type: ignore
from bs4 import BeautifulSoup

load_dotenv("local.env")

BASE_URL = str(getenv("BACKOFFICE_URL"))
LOGIN_URL = BASE_URL + "/"
REPORT_URL = BASE_URL + "/workspace/backoffice/useradministration/userreport"

USERNAME = str(getenv("USERNAME"))
PASSWORD = str(getenv("PASSWORD"))

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": BASE_URL,
}

def get_hidden_fields(html):
    soup = BeautifulSoup(html, "html.parser")
    fields = {}
    for name in ["__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION", "__PREVIOUSPAGE"]:
        tag = soup.find("input", {"name": name})
        if tag and "value" in tag.attrs:
            fields[name] = tag["value"]
    return fields

def save_excel_response(resp):
    content_disp = resp.headers.get("Content-Disposition", "")
    match = re.search(r'filename="?([^"]+)"?', content_disp)
    filename = match.group(1) if match else "reporte.xls"
    with open(filename, "wb") as f:
        f.write(resp.content)
    print(f"✅ Reporte guardado como: {filename}")

login_page = session.get(LOGIN_URL, headers=headers)
login_fields = get_hidden_fields(login_page.text)

login_data = {
    "__VIEWSTATE": login_fields.get("__VIEWSTATE", ""),
    "__VIEWSTATEGENERATOR": login_fields.get("__VIEWSTATEGENERATOR", ""),
    "__EVENTVALIDATION": login_fields.get("__EVENTVALIDATION", ""),
    "__EVENTTARGET": "",
    "__EVENTARGUMENT": "",
    "ctl00$ucHeaderInstitutional$ucLogin$UserName$txt": USERNAME,
    "ctl00$ucHeaderInstitutional$ucLogin$Password$txt": PASSWORD,
    "ctl00$ucHeaderInstitutional$ucLogin$LoginButton": "INGRESAR"
}

login_headers = headers.copy()
login_headers["Referer"] = LOGIN_URL

resp_login = session.post(LOGIN_URL, data=login_data, headers=login_headers)


report_page = session.get(REPORT_URL, headers=headers)
report_fields = get_hidden_fields(report_page.text)


report_data = {
    "__VIEWSTATE": report_fields.get("__VIEWSTATE", ""),
    "__VIEWSTATEGENERATOR": report_fields.get("__VIEWSTATEGENERATOR", ""),
    "__EVENTVALIDATION": report_fields.get("__EVENTVALIDATION", ""),
    "__PREVIOUSPAGE": report_fields.get("__PREVIOUSPAGE", ""),
    "__EVENTTARGET": "",
    "__EVENTARGUMENT": "",
    "ctl00$ContentWeb$vd$btnExportExcel": "Exportar a Excel"
}

report_headers = headers.copy()
report_headers["Referer"] = REPORT_URL

resp_excel = session.post(REPORT_URL, data=report_data, headers=report_headers)
save_excel_response(resp_excel)
