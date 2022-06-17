"""
versiyon ->web için flask ile entegre ediliyor

not : sadece link çekebiliyor
not2: bu versiyonu tekrar düzenleyip ana bir .py dosyası için modül haline getirmeliyim.
"""
from bs4 import BeautifulSoup
from icecream import ic
import requests as rq



def linkFinder_smart(linksVar, url):
    global linkKeeper
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
            link_name = link.text.replace("\n", "").replace(" ", "")
            # print("{} : {}".format(link_name, linkR))
        except TypeError:  # 'https://www.webtekno.com/' sitesinde boş 'href' örneğine rastladım
            pass  # başka sitelerde de olabilir o yüzden buraya koydum

        linkList.append(linkR)
    linkKeeper = []
    linkKeeper = linkList


def GetLink(url, firstList, secondList, control_Filter):
    global linkList
    global content_value
    global c_find
    linkList = []
    c_find = False
    rq_con = rq.get(url)

    soup = BeautifulSoup(rq_con.content, 'html.parser')

    if secondList != [''] and firstList != [''] and control_Filter != True:

        global content

        try:
            # print("\n      ______________________Links______________________\n")
            # ekstra filtre esnasında oluşan hatadan önce "links" yazısı çıkmaması için her koşula ayrı ayrı koydum
            content = soup.find_all(str(firstList[0]), {str(firstList[1]): str(firstList[2])})

            for e in range(len(content)):

                for each in range(0, len(content[e].contents)):

                    try:
                        content_value = e
                        # hata ayıklamya ihtiyaç vardı çünkü for içinde gezinirken hatalar ortaya çıkıyor
                        community = content[e].contents[each]
                        filter2 = community.find_all(str(secondList[0]), {str(secondList[1]): str(secondList[2])})

                        for each2 in range(len(filter2)):
                            # print(f"\n      ______________________[{each},{each2}]______________________")
                            links = filter2[each2].find_all("a")
                            linkFinder_smart(links, url)

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
        # print("\n      ______________________Links______________________\n")
        # ekstra filtre esnasında oluşan hatadan önce "links" yazısı çıkmaması için her koşula ayrı ayrı koydum
        linkFinder_smart(links, url)




    elif firstList != [''] and control_Filter:

        if len(nums) == 2:
            # extraFilter iki parametre de boş olmazsa kullnılabilir olan bu olacak
            community = content[content_value].contents[int(nums[0])]
            extraF = community.find_all(str(secondList[0]), {str(secondList[1]): str(secondList[2])})

            links = extraF[int(nums[1])].find_all("a")

            # print("\n      ______________________Links______________________\n")
            # ekstra filtre esnasında oluşan hatadan önce "links" yazısı çıkmaması için her koşula ayrı ayrı koydum
            linkList = []
            linkFinder_smart(links, url)

        elif len(nums) == 1:
            # sadece ilk parametre dolu olduğunda kullanılabilir olacak
            extraF = content[int(nums[0])]
            links = extraF.find_all("a")
            # print(f"\n      ______________________[{nums[0]}]______________________")
            linkFinder_smart(links, url)
            """BURADA KALDIN!"""

    else:
        content = soup.find_all(str(firstList[0]), {str(firstList[1]): str(firstList[2])})

        # print("\n      ______________________Links______________________\n")
        # ekstra filtre esnasında oluşan hatadan önce "links" yazısı çıkmaması için her koşula ayrı ayrı koydum
        for e in range(len(content)):
            # print(f"\n      ______________________[{e}]______________________")
            for each in range(0, len(content[e].contents)):
                content_value = e

                try:
                    links = content[e].contents[each].find_all("a")
                    linkFinder_smart(links, url)

                except AttributeError:
                    continue
                except IndexError:
                    continue

    if len(linkList) == 0:
        pass
        # print("Bir hatadan ötürü linkler bulunamadı ya da hiç link yok!")
    else:
        pass
        # print("\n___________________________________" + ("_" * len(str(len(linkList)))))  # sadece simetri için
        # uğraştım print(f"________{len(linkList)} adet link bulundu!________")


def MainLinkGetter(url, parameter1='', parameter2=''):
    global nums
    control_extraFilter = False

    if url[:4] == "http":
        firstList = parameter1.split(".")
        secondList = parameter2.split(".")
        GetLink(url, firstList, secondList, control_extraFilter)
        sayac = "=>"+str(len(linkKeeper))+" adet link bulundu!"
        return [linkKeeper, sayac]

    else:
        return [["______hatalı adres!______"]]


"""
        if len(linkList)!=0 and firstList!=['']:
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
                    #print(no_bug)

                    if no_bug:
                        break
                    else:
                        pass

                else:
                    break

            except ValueError:
                no_bug = False
                #print("Hatalı değer girdiniz!\n")
                continue

            except IndexError:
                no_bug = False
                #print("Bu değerlerde filterelenecek bir şey yok!!\n")
                continue

    else:
        #print("\n_________________________\n______hatalı adres!______")
        """

#a = MainLinkGetter("https://www.aviationweather.gov/", "div.id.awc_botnav", "ul..")