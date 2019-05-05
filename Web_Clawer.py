import requests
from bs4 import BeautifulSoup
import xlwt
from xlwt import Workbook
import re


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def date_formate_transfer(original_date_formate):
    if 'January' in original_date_formate:
        return original_date_formate.split('January')[1]+'-'+'1'+'-'+original_date_formate.split('January')[0]
    if 'February' in original_date_formate:
        return original_date_formate.split('February')[1]+'-'+'2'+'-'+original_date_formate.split('February')[0]
    if 'March' in original_date_formate:
        return original_date_formate.split('March')[1]+'-'+'3'+'-'+original_date_formate.split('March')[0]
    if 'April' in original_date_formate:
        return original_date_formate.split('April')[1]+'-'+'4'+'-'+original_date_formate.split('April')[0]
    if 'May' in original_date_formate:
        return original_date_formate.split('May')[1]+'-'+'5'+'-'+original_date_formate.split('May')[0]
    if 'June' in original_date_formate:
        return original_date_formate.split('June')[1]+'-'+'6'+'-'+original_date_formate.split('June')[0]
    if 'July' in original_date_formate:
        return original_date_formate.split('July')[1]+'-'+'7'+'-'+original_date_formate.split('July')[0]
    if 'August' in original_date_formate:
        return original_date_formate.split('August')[1]+'-'+'8'+'-'+original_date_formate.split('August')[0]
    if 'September' in original_date_formate:
        return original_date_formate.split('September')[1]+'-'+'9'+'-'+original_date_formate.split('September')[0]
    if 'October' in original_date_formate:
        return original_date_formate.split('October')[1]+'-'+'10'+'-'+original_date_formate.split('October')[0]
    if 'November' in original_date_formate:
        return original_date_formate.split('November')[1]+'-'+'11'+'-'+original_date_formate.split('November')[0]
    if 'December' in original_date_formate:
        return original_date_formate.split('December')[1]+'-'+'1'+'-'+original_date_formate.split('December')[0]
    else:
        return original_date_formate


def KobeBryant():
    content = requests.get('https://en.wikipedia.org/wiki/Kobe_Bryant').content
    soup = BeautifulSoup(content,'html.parser')
    for table in soup.find_all('table',{'class':'infobox vcard'}):
        print table.text.strip()

def MPs_general_election_from_1997_to_2015():
    years_of_election = {2015}
    for year_of_election in years_of_election:
        book = Workbook(encoding='utf-8')
        sheet1 = book.add_sheet(str(year_of_election))
        sheet1.write(0, 0, 'Name')
        sheet1.write(0, 1, 'Birth')
        sheet1.write(0, 2, 'University')
        sheet1.write(0, 3, 'Party')
        sheet1.write(0, 4, 'Term of Constitution')
        sheet1.write(0, 5, 'Constitution')
        sheet1.write(0, 6, 'Term of Prime Minister')
        sheet1.write(0, 7, 'Leader')
        sheet1.write(0, 8, 'Department')
        sheet1.write(0, 9, 'Term of Department')
        url = 'https://en.wikipedia.org/wiki/List_of_MPs_elected_in_the_United_Kingdom_general_election,_'+str(year_of_election)
        print url
        content = requests.get(url).content
        soup = BeautifulSoup(content,'html.parser')
        table = soup.find_all('table',{'class':'wikitable'})[1]
        rows_number = (len(table.find_all('tr')))
        folder_name = '/Users/jiaminghuang/Desktop/test/'+str(year_of_election)+'/'
        row_count = 2
        for row in table.find_all('tr')[1:rows_number]:
            cols_number = (len(row.find_all('td')))
            leader = 0
            member_name = ''
            bday = ''
            university = ''
            political_party=''
            in_office1=[]
            consitution=[]
            dpt = []
            dpt_time=[]
            prim_minis=''
            state = row.find_all('td')[5].get_text()
            if not 'Seat held' in state:
                col = row.find_all('td')
                a = col[4].find('a')
                member_name = a.get_text()
                link = a.get('href')
                content = requests.get('https://en.wikipedia.org'+link).content
                soup = BeautifulSoup(content, 'html.parser')
                for table in soup.find_all('table', {'class': 'infobox vcard'}):
                    #f =file(folder_name+member_name+'.txt','a')
                    #print>>f,table.text.strip()
                    #f.close()
                    for header in table.find_all('th')[0:(len(table.find_all('th')))]:
                        text = header.get_text()
                        if('Prime Minister of' in header.get_text()):
                            pm = header.find_next('td').get_text()
                            p = r'\d+ *\w+ *\d*'
                            pattern1 = re.compile(p)
                            pmday = pattern1.findall(pm)
                            if len(pmday)<2:
                                prim_minis = 'unknown'
                            else:
                                pmday1 = pmday[0] + '-' + pmday[1]
                                prim_minis = pmday1
                            print pmday1
                        elif('Leader of' in header.get_text() and not 'Opposition' in header.get_text()):
                            leader = 1
                        elif ('Leader of' in header.get_text() and 'Opposition' in header.get_text()):
                            print 'oppo'
                        elif ('Personal details' in header.get_text()):
                            print 'Personal details'
                        elif(header.get_text()=='Born'):
                            bday1 = header.find_next_sibling('td').get_text()
                            p = r'[0-9]+ [A-Z]+[a-z]+ [0-9]+'
                            pattern1 = re.compile(p)
                            bday2 = str(pattern1.findall(bday1))
                            bday = str(date_formate_transfer(bday2[3:len(bday2)-2]))+" "+ bday
                            print bday
                        elif('Member of Parliament' in header.get_text()):
                            in_office1.append(header.find_next('td').get_text().split('\n')[1])
                            #consitution.append(header.get_text().split('for')[1])
                            aa = header.find_all('a')
                            a = aa[len(aa)-1]
                            consitution.append(a.get_text())
                            print member_name
                            print consitution
                            print in_office1
                        elif ('Alma mater' in header.get_text()):
                            university = header.find_next('td').get_text()+","+university
                            print university
                        elif ('Political party' in header.get_text()):
                            political_party = header.find_next('td').get_text()+','+political_party
                            print political_party
                        else :
                            #atts = header.attrs
                            if('lavender' in str(header.attrs)):
                                dt = header.find_next('td').get_text()
                                p = r'\d+ *\w+ *\d*'
                                pattern1 = re.compile(p)
                                dtday = pattern1.findall(dt)
                                if len(dtday)>1:
                                    dpt.append(header.get_text())
                                    dtday1 = dtday[0] + '-' + dtday[1]
                                    dpt_time.append(dtday1)
                                    print dtday1
            for index_cons in range(0,len(consitution)):
                if len(dpt) == 0:
                    sheet1.write(row_count, 0, member_name)
                    sheet1.write(row_count, 1, bday)
                    sheet1.write(row_count, 2, university)
                    sheet1.write(row_count, 3, political_party)
                    sheet1.write(row_count, 4, in_office1[index_cons])
                    sheet1.write(row_count, 5, consitution[index_cons])
                    sheet1.write(row_count, 6, prim_minis)
                    sheet1.write(row_count, 7, leader)
                    row_count = row_count + 1
                    print row_count
                else:
                    for index_dep in range(0, len(dpt)):
                        sheet1.write(row_count, 0, member_name)
                        sheet1.write(row_count, 1, bday)
                        sheet1.write(row_count, 2, university)
                        sheet1.write(row_count, 3, political_party)
                        sheet1.write(row_count, 4, in_office1[index_cons])
                        sheet1.write(row_count, 5, consitution[index_cons])
                        sheet1.write(row_count, 6, prim_minis)
                        sheet1.write(row_count, 7, leader)
                        sheet1.write(row_count, 8, dpt[index_dep])
                        sheet1.write(row_count, 9, dpt_time[index_dep])
                        row_count = row_count + 1
                        print row_count

        book.save('/Users/jiaminghuang/Desktop/test1/'+str(year_of_election)+'.xls')



if __name__ == '__main__':
    MPs_general_election_from_1997_to_2015()