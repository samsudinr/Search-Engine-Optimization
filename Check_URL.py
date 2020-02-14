import init
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
start_time = time.clock()
def Get_data(link, user_agent, user_agent2):
    page = requests.get(link, headers=user_agent)
    page2 = requests.get(link, headers=user_agent2)
    soup = BeautifulSoup(page.text, 'lxml')
    Meta_data = []
    link_canonical = []
    Redirect_URL = []
    if page.status_code == 200:
        try:
            get_link = soup.find('link', attrs={"rel": "canonical"})['href']
            link_canonical.append(get_link.encode('utf-8'))
        except:
            link_canonical.append("Request 200 and Canonical not Found")
        if soup.title == None:
            title = 'Request [200] but Title Not Found'
        else:
            title = (soup.title.string)
        try:
            get_desc = soup.find('meta', attrs={'name':'description'})["content"]
            description = get_desc.encode('utf-8')
        except:
            description = 'Request [200] complete but Description Not Found'
        try:
            get_key = soup.find('meta', attrs={'name': 'keywords'})["content"]
            keyword = get_key.encode('utf-8')
        except:
            keyword = 'Request [200] but Description Not Found'
        Meta_data.extend((title, description, keyword))
    elif page.status_code == 404:
        link_canonical.append("Request 404 and Canonical not Found")
        if soup.title == None:
            title = 'Request [404] and Title Not Found'
        else:
            title = (soup.title.string)
        try:
            get_desc = soup.find('meta', attrs={'name': 'description'})["content"]
            description = get_desc.encode('utf-8')
        except:
            description = 'Request [404] and Content Description Not Found'
        try:
            get_key = soup.find('meta', attrs={'name': 'keywords'})["content"]
            keyword = get_key.encode('utf-8')
        except:
            keyword = 'Request [404] and Content Keywords Not Found'
        Meta_data.extend((title, description, keyword))
    else:
        try:
            get_link = soup.find('link', attrs={"rel": "canonical"})['href']
            link_canonical.append(get_link.encode('utf-8'))
        except:
            link_canonical.append("Check-Status code and Page not founds")
        Meta_data.extend(("CHECK-Page and Title is not found", "CHECK-Page and Description is not found","CHECK-Page and keywords is not found"))

    if page2.status_code == 200:
        Redirect_URL.append(page2.url)
    elif page2.status_code == 404:
        Redirect_URL.append(page2.url)
    else:
        Redirect_URL.append("CHECK-Redirect and Page not Founds")
    get_value = [Meta_data, link_canonical, Redirect_URL]
    return get_value

def redirect_URL(link, user_agent):
    page = requests.get(link, headers=user_agent)
    if page.status_code == 200:
        return page.url
    elif page.status_code == 404:
        return page.url
    else:
        return 'CHECK-Page is not found'

def meta_all(link, user_agent):
    page = requests.get(link, headers=user_agent)
    soup = BeautifulSoup(page.text, 'lxml')
    metas = soup.find_all('meta')
    if page.status_code == 200:
        if soup.title == None:
            title = 'None'
        else:
            title = (soup.title.string)
        description = [meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description']
        keyword = [meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'keywords']
        return [title, description, keyword]
    elif page.status_code == 404:
        if soup.title == None:
            title = 'None'
        else:
            title = (soup.title.string)
        description = [meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description']
        keyword = [meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'keywords']
        return [title, description, keyword]
    else:
        return ["CHECK-Page and Title is not found", "CHECK-Page and Description is not found", "CHECK-Page and keywords is not found"]

def upload_and_replace_file(Directory_file, ID_file_for_replace_content_file, initDict):
    """
    :param Directory_file: Directory file local to replace content a file in google drive
    :param ID_file_for_replace_content_file: ID a file in google drive
    :return:
    """
    gauth = GoogleAuth()
    # load cline credentials with path dir, you must change the name of client_secrets.json
    gauth.LoadClientConfigFile(initDict['pathClientSecret'])
    # Try to load saved client credentials
    gauth.LoadCredentialsFile(initDict['pathTokenDrive'])
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile(initDict['pathTokenDrive'])

    drive = GoogleDrive(gauth)
    # read file from google drive with ID name
    read_data = drive.CreateFile({'id': ID_file_for_replace_content_file})
    # function for replace content a file in google drive with content file local
    read_data.SetContentFile(Directory_file)
    read_data.Upload({'convert': True})

# read data dekstop and mobil, copy the data, and write to new excel
data_dekstop = pd.read_excel(init.filename1, sheet_name="Dekstop")
copy_data_dekstop_1 = data_dekstop.copy()
# copy_data_dekstop_2 = data_dekstop.copy()
# copy_data_dekstop_3 = data_dekstop.copy()
data_dekstop.to_excel(init.writerss, sheet_name='Dekstop URL', index=False)

data_mobile = pd.read_excel(init.filename1, sheet_name="Mobile")
# copy_data_mobile_1 = data_mobile.copy()
# copy_data_mobile_2 = data_mobile.copy()
# copy_data_mobile_3 = data_mobile.copy()
data_mobile.to_excel(init.writerss, sheet_name='Mobile URL', index=False)

data_dekstop['all'] = data_dekstop['Page URL'].apply(lambda x: Get_data(x, init.headers_dekstop, init.headers_mobile))
data_dekstop['Meta'] = data_dekstop['all'].apply(lambda x: x[0])
data_dekstop['Canonical URL'] = data_dekstop['all'].apply(lambda x: x[1])
data_dekstop['Ridirect URL'] = data_dekstop['all'].apply(lambda x: x[2])

data_dekstop['Title'] = data_dekstop['Meta'].apply(lambda x: x[0])
data_dekstop['Description'] = data_dekstop['Meta'].apply(lambda x: x[1])
data_dekstop['Keywords'] = data_dekstop['Meta'].apply(lambda x: x[2])

# dekstop_link = data_dekstop[['Page URL']]
# dekstop_link.to_excel(init.writerss, sheet_name="Sitemap URL", index=False)
dekstop_canonical = data_dekstop[['Page URL', 'Canonical URL']]
dekstop_canonical.to_excel(init.writerss, sheet_name="Dekstop Canonical", index=False)
dekstop_meta = data_dekstop[['Page URL', 'Title', 'Description', 'Keywords']]
dekstop_meta.to_excel(init.writerss, sheet_name="Dekstop Meta", index=False)
dekstop_redirect = data_dekstop[['Page URL', 'Ridirect URL']]
dekstop_redirect.to_excel(init.writerss, sheet_name="Redirect URL Dekstop to Mobile", index=False)
time.sleep(5)
data_mobile['all'] = data_mobile['Page URL'].apply(lambda x: Get_data(x, init.headers_mobile, init.headers_dekstop))
data_mobile['Meta'] = data_mobile['all'].apply(lambda x: x[0])
data_mobile['Canonical URL'] = data_mobile['all'].apply(lambda x: x[1])
data_mobile['Redirect URL'] = data_mobile['all'].apply(lambda x: x[2])

data_mobile['Title'] = data_mobile['Meta'].apply(lambda x: x[0])
data_mobile['Description'] = data_mobile['Meta'].apply(lambda x: x[1])
data_mobile['Keywords'] = data_mobile['Meta'].apply(lambda x: x[2])

mobile_canonical = data_mobile[['Page URL', 'Canonical URL']]
mobile_canonical.to_excel(init.writerss, sheet_name="Mobile Canonical", index=False)
mobile_meta = data_mobile[['Page URL', 'Title', 'Description', 'Keywords']]
mobile_meta.to_excel(init.writerss, sheet_name="Mobile Meta", index=False)
mobile_redirect = data_mobile[['Page URL', 'Redirect URL']]
mobile_redirect.to_excel(init.writerss, sheet_name="Redirect URL Mobile to Dekstop", index=False)
time.sleep(5)
# ## process to get canonical url data dekstop dan mobil, and write to new excel
# copy_data_dekstop_1['Canonical URL'] = copy_data_dekstop_1['Page URL'].apply(lambda x: Check_canonical(x, init.headers_dekstop))
# copy_data_dekstop_1.to_excel(init.writerss, sheet_name="Dekstop Canonical", index=False)
# time.sleep(5)
#
# copy_data_mobile_1['Canonical URL'] = copy_data_mobile_1['Page URL'].apply(lambda x: Check_canonical(x, init.headers_mobile))
# copy_data_mobile_1.to_excel(init.writerss, sheet_name="Mobile Canonical", index=False)
# time.sleep(5)

# # process to get meta title, description, and keywords from dekstop dan mobile url, and write to new excel
# copy_data_dekstop_2['Meta'] = copy_data_dekstop_2['Page URL'].apply(lambda x: meta_all(x, init.headers_dekstop))
# copy_data_dekstop_2['Title'] = copy_data_dekstop_2['Meta'].apply(lambda x: x[0])
# copy_data_dekstop_2['Description'] = copy_data_dekstop_2['Meta'].apply(lambda x:[1])
# copy_data_dekstop_2['Keywords'] = copy_data_dekstop_2['Meta'].apply(lambda x:[2])
# copy_data_dekstop_2.to_excel(init.writerss, sheet_name='Dekstop Meta', index=False)
# time.sleep(5)
#
# copy_data_mobile_2['Meta'] = copy_data_mobile_2['Page URL'].apply(lambda x: meta_all(x, init.headers_mobile))
# copy_data_mobile_2['Title'] = copy_data_mobile_2['Meta'].apply(lambda x: x[0])
# copy_data_mobile_2['Description'] = copy_data_mobile_2['Meta'].apply(lambda x: x[1])
# copy_data_mobile_2['Keywords'] = copy_data_mobile_2['Meta'].apply(lambda x: x[2])
# copy_data_mobile_2.to_excel(init.writerss, sheet_name='Mobile Meta', index=False)
# time.sleep(5)
#
# copy_data_dekstop_3['Redirect URL'] = copy_data_dekstop_3['Page URL'].apply(lambda x: redirect_URL(x, init.headers_mobile))
# copy_data_dekstop_3.to_excel(init.writerss, sheet_name='Redirect URL Dekstop to Mobile', index=False)
# time.sleep(5)
#
# copy_data_mobile_3['Redirect URL'] = copy_data_mobile_3['Page URL']. apply(lambda x: redirect_URL(x, init.headers_dekstop))
# copy_data_mobile_3.to_excel(init.writerss, sheet_name='Redirect URL Mobile to Dekstop', index=False)
# time.sleep(5)
#
init.writerss.save()
init.writerss.close()
#
upload_and_replace_file(init.filename2, init.ID_for_upload_File, init.cred_emcanalyticsteam)
print("--- %s seconds ---" % (time.clock() - start_time))
