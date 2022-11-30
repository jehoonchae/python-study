from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv

CHROME_DRIVER = ''  # 크롬 경로 입력
driver = webdriver.Chrome(CHROME_DRIVER)
time.sleep(1)
url = 'http://www.dbpia.co.kr/journal/publicationDetail?publicationId=PLCT00006711'
driver.get(url)
# sleep_time = random.random()*3
time.sleep(3)

OUTPUT_FILE_NAME = '.csv'  # csv 파일 이름 정하기

with open(OUTPUT_FILE_NAME, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['author', 'date', 'kor_title', 'eng_title', 'kor_abstract', 'eng_abstract'])
    for i in range(20):
        for j in range(4):
            try:
                # driver.execute_script("window.scrollTo(0, 0)")
                driver.find_element_by_xpath(f'//*[@id="voisList"]/li[{i + 2}]/a').click()
                driver.find_element_by_xpath(f'//*[@id="voisList"]/li[{i + 2}]/div/div/ul/li[{j + 1}]/a').click()
                time.sleep(1)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                page_num = soup.find('div', class_='infoWrap').find_all('dl')[-1].find('dd').text
                for k in range(int(page_num)):
                    try:
                        if soup.find('p', class_='session') == None:  # 세션 구분이 없는 호
                            driver.find_element_by_xpath(f'//*[@id="voisNodeList"]/ul/li[{k + 1}]/div/div[2]/h5/a').click()
                            time.sleep(1)
                            html = driver.page_source
                            soup = BeautifulSoup(html, 'lxml')
                            if soup.find('p', class_='article') == None:  # 목차
                                driver.back()
                                time.sleep(1)
                            elif len(soup.find_all('p', class_='article')) == 1:  # 영어 논문
                                eng_title = soup.find('span', class_='articleTitle').text.strip()
                                eng_abstract = soup.find_all('p', class_='article')[0].text.strip()
                                author = soup.find('a', target='_blank').text.strip()
                                date = soup.find('li', class_='date').text.strip()
                                writer.writerow([author, date, ' ', eng_title, ' ', eng_abstract])
                                driver.back()
                                time.sleep(1)
                            else:  # 국문 논문
                                kor_title = soup.find('span', class_='articleTitle').text.strip()
                                eng_title = soup.find('span', class_='equalTitle').text.strip()
                                kor_abstract = soup.find_all('p', class_='article')[0].text.strip()
                                eng_abstract = soup.find_all('p', class_='article')[1].text.strip()
                                author = soup.find('a', target='_blank').text.strip()
                                date = soup.find('li', class_='date').text.strip()
                                writer.writerow([author, date, kor_title, eng_title, kor_abstract, eng_abstract])
                                driver.back()
                                time.sleep(1)
                        else:  # 세션 구분이 있는 호
                            if k == int(page_num):
                                continue
                            else:
                                driver.find_element_by_xpath(f'//*[@id="voisNodeList"]/ul[2]/li[{k + 1}]/div/div[2]/h5/a').click()
                                time.sleep(1)
                                html = driver.page_source
                                soup = BeautifulSoup(html, 'lxml')
                                if soup.find('p', class_='article') == None:  # 목차
                                    driver.back()
                                    time.sleep(1)
                                elif len(soup.find_all('p', class_='article')) == 1:  # 영어 논문
                                    eng_title = soup.find('span', class_='articleTitle').text.strip()
                                    eng_abstract = soup.find_all('p', class_='article')[0].text.strip()
                                    author = soup.find('a', target='_blank').text.strip()
                                    date = soup.find('li', class_='date').text.strip()
                                    writer.writerow([author, date, ' ', eng_title, ' ', eng_abstract])
                                    driver.back()
                                    time.sleep(1)
                                else:  # 국문 논문
                                    kor_title = soup.find('span', class_='articleTitle').text.strip()
                                    eng_title = soup.find('span', class_='equalTitle').text.strip()
                                    kor_abstract = soup.find_all('p', class_='article')[0].text.strip()
                                    eng_abstract = soup.find_all('p', class_='article')[1].text.strip()
                                    author = soup.find('a', target='_blank').text.strip()
                                    date = soup.find('li', class_='date').text.strip()
                                    writer.writerow([author, date, kor_title, eng_title, kor_abstract, eng_abstract])
                                    driver.back()
                                    time.sleep(1)
                    except:  # 수집되지 않은 논문 정보 출력
                        print(str(2019 - i) + '년 ' + str(4 - j) + '호 ' + str(k + 1) + "번째 수집되지 않음")
            except:
                print(str(2019 - i) + '년' + str(j) + '번째 호 없음')