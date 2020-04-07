from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

##########################################
###  Fetching Python-related job data  ###
##########################################

print('FETCHING DATA...\n')

indeed = 'https://www.indeed.co.za/jobs?q=python+developer&l=Cape+Town%2C+Western+Cape'
careers24 = 'https://www.careers24.com/jobs/kw-python-developer/m-true/'
pnet = 'https://www.pnet.co.za/5/job-search-detailed.html?stf=freeText&ns=1&qs=%5B%7B%22id%22%3A%2223000176%22%2C%22description%22%3A%22Cape+Town%22%2C%22type%22%3A%22geocity%22%7D%5D&companyID=0&cityID=23000176&sourceOfTheSearchField=resultlistpage%3Ageneral&searchOrigin=Resultlist_top-search&ke=python+developer&ws=Cape+Town&ra=30&sat=where'

r_indeed = requests.get(indeed).content
r_careers24 = requests.get(careers24).content
r_pnet = requests.get(pnet).content

soup_indeed = BeautifulSoup(r_indeed, 'html.parser')
soup_careers24 = BeautifulSoup(r_careers24, 'html.parser')
soup_pnet = BeautifulSoup(r_pnet, 'html.parser')


###################################################
###  Functions to add first page data to lists  ###
###################################################

indeed_desc = []
indeed_links = []

careers24_desc = []
careers24_links = []

pnet_desc = []
pnet_links = []


def get_indeed():

    for job in soup_indeed.find_all('div', {'class': 'title'}):
        indeed_desc.append(job.text.replace('\n', ''))
        indeed_links.append('www.indeed.co.za' + (job.find('a')['href']))


def get_careers24():

    for job in soup_careers24.find_all('div', {'class': 'span6 job_search_content'}):
        careers24_desc.append(job.span.text)
        careers24_links.append('www.careers24.com' + (job.find('a')['href']))


def get_pnet():

    for job in soup_pnet.find_all('div', {'class': 'styled__JobItemFirstLineWrapper-sc-11l5pt9-2 fuVwNh'}):
        pnet_desc.append(job.a.text)
        pnet_links.append('www.pnet.co.za' + (job.find('a')['href']))


get_indeed()
get_careers24()
get_pnet()

#########################################
###  Combining data and prioritizing  ###
#########################################
print('COMBINING DATA...\n')

top_selection = '\nMOST RELEVANT:\n\n\n'
indeed_email = 'INDEED RESULTS:\n\n\n'
careers24_email = 'CAREERS24 RESULTS:\n\n\n'
pnet_email = 'PNET RESULTS:\n\n\n'

for i in range(len(indeed_desc)):

    if 'python' in indeed_desc[i].lower():
        top_selection += f'{indeed_desc[i]}\n{indeed_links[i]}\n\n\n'
    elif 'internship' in indeed_desc[i].lower():
        top_selection += f'{indeed_desc[i]}\n{indeed_links[i]}\n\n\n'
    else:
        indeed_email += f'{indeed_desc[i]}\n{indeed_links[i]}\n\n\n'


for i in range(len(careers24_desc)):

    if 'python' in careers24_desc[i].lower():
        top_selection += f'{careers24_desc[i]}\n{careers24_links[i]}\n\n\n'
    elif 'internship' in careers24_desc[i].lower():
        top_selection += f'{careers24_desc[i]}\n{careers24_links[i]}\n\n\n'
    else:
        careers24_email += f'{careers24_desc[i]}\n{careers24_links[i]}\n\n\n'


for i in range(len(pnet_desc)):

    if 'python' in pnet_desc[i].lower():
        top_selection += f'{pnet_desc[i]}\n{pnet_links[i]}\n\n\n'
    elif 'internship' in pnet_desc[i].lower():
        top_selection += f'{pnet_desc[i]}\n{pnet_links[i]}\n\n\n'
    else:
        pnet_email += f'{pnet_desc[i]}\n{pnet_links[i]}\n\n\n'



########################################
###  Send email from email to email  ###
########################################

print('BUILDING EMAIL...\n')

s = smtplib.SMTP(host='smtp.gmail.com', port=587)

s.ehlo()
s.starttls()
s.login('--InsertEmailHere', '--InsertPasswordHere--')

msg = MIMEMultipart()

content = f'{top_selection}{indeed_email}{careers24_email}{pnet_email}'

msg['From'] = 'InsertFromEmail'
msg['To'] = 'InsertToEmail'
msg['Subject'] = 'Job Fish'

msg.attach(MIMEText(content, 'plain'))
s.send_message(msg)
s.close()

print('EMAIL SENT.')