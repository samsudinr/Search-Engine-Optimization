import pandas as pd

# first process to write excel file for saving all page URL to dekstop and mobile
filename1 = "Toyota_sitemap_url.xlsx"
writer = pd.ExcelWriter(filename1)

# second file for read all page URL and get canonical, meta description.
filename2 = "Toyota Sitemap URL 2.xlsx"
writerss = pd.ExcelWriter(filename2, engine='openpyxl')

url_mobile = "https://m.toyota.astra.co.id/sitemap.xml"
url_dekstop = "https://www.toyota.astra.co.id/sitemap.xml"

headers_dekstop = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
headers_mobile = {'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'}

ID_for_upload_File = "ID_google_Spreadsheet"

cred_emcanalyticsteam = {
    'pathClientSecret': 'cred/client_secret_emcanalyticsteam.json',
    'pathTokenDrive': 'cred/token_drive_emcanalyticsteam.pickle'
}
