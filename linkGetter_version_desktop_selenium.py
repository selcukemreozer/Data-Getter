"""
versiyon -> masaüstü uygulaması

not : sadece link çekebiliyor
not2: bu versiyonu tekrar düzenleyip ana bir .py dosyası için modül haline getirmeliyim.
"""
from bs4 import BeautifulSoup
from icecream import ic
import requests as rq
from selenium import webdriver

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
global url


def LinkFinder_smart(linksVar):
    for link in linksVar:
        linkR = link.get("href")

        try:
            if linkR[:4] == "http":  # bazı linklerde site ismi olmuyor onu kontrol edip eksikse tamamlayan bir yapı
                pass

            elif linkR[:2] == "//":  # bazı linklerde site ismi var ama http eklentisi yok
                linkR = "https:" + linkR

            elif linkR[:len(url)] != url:
                linkR = linkR.replace("/", "", 1)
                linkR = url + linkR

            else:
                pass
            link_name = link.text.replace("\n", "").replace(" ", "").replace("  ", "")
            print("{} : {}".format(link_name, linkR))
        except TypeError:  # 'https://www.webtekno.com/' sitesinde boş 'href' örneğine rastladım
            pass  # başka sitelerde de olabilir o yüzden buraya koydum

        linkList.append(linkR)


def GetLink(link, firstList, secondList, control_Filter):
    global linkList
    global content_value
    global c_find
    linkList = []
    source = ''
    c_find = False

    # rq_con = rq.get(link)
    chromeOptions = Options()
    chromeOptions.add_argument("--headless")
    chromeOptions.add_argument("--window-size=1920x1080")


    driver = webdriver.Chrome('C:\\Users\\selcukemre\\Desktop\\chromedriver.exe', options=chromeOptions)
    # soup = BeautifulSoup(rq_con.content, 'html.parser')
    driver.get(link)
    # bu bir lavascript kodu scrollu hareket ettirmeni sağlıyor.
    # Bunu masaüstündeki dataThief/selenium_scroll.txt dosyasında anlatıyorum
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    ic(lastHeight)
    i = 0
    while True:  # i<4
        actions = ActionChains(driver)
        actions.send_keys(Keys.PAGE_DOWN)
        #actions.perform()
        #actions.send_keys(Keys.ARROW_DOWN)
        actions.perform()

        source += driver.page_source
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(6)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        ic(type(driver.execute_script("return document.body.scrollHeight")))
        ic(newHeight)

        if newHeight == lastHeight:
            ic()
            break
        else:
            lastHeight = newHeight
            ic(lastHeight)

        i = i + 1

    soup = BeautifulSoup(source, 'html.parser')
    driver.quit()

    if secondList != [''] and firstList != [''] and control_Filter != True:

        global content

        try:
            print("\n      ______________________Links______________________\n")
            # ekstra filtre esnasında oluşan hatadan önce "links" yazısı çıkmaması için her koşula ayrı ayrı koydum
            content = soup.find_all(str(firstList[0]), {str(firstList[1]): str(firstList[2])})

            for e in range(len(content)):

                for each in range(0, len(content[e].contents)):

                    try:
                        content_value = e
                        # hata ayıklamya ihtiyaç vardı çünkü for içinde gezinirken hatalar ortaya çıkıyor
                        community = content[e].contents[each]
                        filter2 = community.find_all(str(secondList[0]), {str(secondList[1]): str(secondList[2])})
                        links = filter2[0].find_all("a")

                        for each2 in range(len(filter2)):
                            print(f"\n      ______________________[{each},{each2}]______________________")
                            links = filter2[each2].find_all("a")
                            LinkFinder_smart(links)

                            c_find = False
                            """
                            Bu döngü şu yüzden var: 2.filtrede 'filter2' değişkeninin 1'den fazla elementinde
                            x.find_all("a") değeri bulunabiliyor. Bu yüzden for ile tüm 'filter2' yürütülüyor.
                            """

                    except AttributeError:
                        continue
                    except IndexError:
                        continue

        except AttributeError:
            pass
        except IndexError:
            pass

    elif secondList == [''] and firstList == ['']:
        # iki parametre de boş bırakılırsa urldeki tüm linkleri bulur
        links = soup.find_all('a')
        print("\n      ______________________Links______________________\n")
        # ekstra filtre esnasında oluşan hatadan önce "links" yazısı çıkmaması için her koşula ayrı ayrı koydum
        LinkFinder_smart(links)

    elif firstList != [''] and control_Filter:

        if len(nums) == 2:
            # extraFilter iki parametre de boş olmazsa kullnılabilir olacak çift parametreli filtreleme
            community = content[content_value].contents[int(nums[0])]
            extraF = community.find_all(str(secondList[0]), {str(secondList[1]): str(secondList[2])})

            links = extraF[int(nums[1])].find_all("a")

            print("\n      ______________________Links______________________\n")
            # ekstra filtre esnasında oluşan hatadan önce "links" yazısı çıkmaması için her koşula ayrı ayrı koydum
            linkList = []
            LinkFinder_smart(links)

        elif len(nums) == 1:
            # sadece ilk parametre dolu olduğunda kullanılabilir olacak tek parametreli filtreleme
            extraF = content[int(nums[0])]
            links = extraF.find_all("a")
            print(f"\n      ______________________[{nums[0]}]______________________")
            LinkFinder_smart(links)

    else:
        content = soup.find_all(str(firstList[0]), {str(firstList[1]): str(firstList[2])})

        print("\n      ______________________Links______________________\n")
        # ekstra filtre esnasında oluşan hatadan önce "links" yazısı çıkmaması için her koşula ayrı ayrı koydum
        for e in range(len(content)):
            print(f"\n      ______________________[{e}]______________________")
            for each in range(0, len(content[e].contents)):
                content_value = e

                try:
                    links = content[e].contents[each].find_all("a")
                    LinkFinder_smart(links)

                except AttributeError:
                    continue
                except IndexError:
                    continue

    if len(linkList) == 0:
        print("Bir hatadan ötürü linkler bulunamadı ya da hiç link yok!")
    else:
        print("\n___________________________________" + ("_" * len(str(len(linkList)))))  # sadece simetri için uğraştım
        print(f"________{len(linkList)} adet link bulundu!________")


def MainLinkGetter():
    global url
    global nums
    control_extraFilter = False
    url = input("url:")

    if url[:4] == "http":

        parameter1 = input("parameter_1:")
        parameter2 = input("parameter_2:")
        firstList = parameter1.split(".")
        secondList = parameter2.split(".")
        GetLink(url, firstList, secondList, control_extraFilter)

        if len(linkList) != 0 and firstList != ['']:
            question = input("\nDo you want use extraFilter? [y/n]:")

        else:
            question = str()

        while True:
            no_bug = True  # hatalı değer girildiğinde döngüyü devam ettiren değişken
            try:

                if question.lower() == "y":
                    control_extraFilter = True
                    extraFilter_ = input("E.F:")
                    nums = extraFilter_.split(",")
                    GetLink(url, firstList, secondList, control_extraFilter)

                    if no_bug:
                        break
                    else:
                        pass

                else:
                    break

            except ValueError:
                no_bug = False
                print("Hatalı değer girdiniz!\n")
                continue

            except IndexError:
                no_bug = False
                print("Bu değerlerde filterelenecek bir şey yok!!\n")
                continue

    else:
        print("\n_________________________\n______hatalı adres!______")


MainLinkGetter()
