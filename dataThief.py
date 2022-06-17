from bs4 import BeautifulSoup
from icecream import ic
import requests as rq


global url
control_extraFilter = False
linkList = []


def linkFinder_smart(linksVar):

    for link in linksVar:

        linkR = link.get("href")
        ic(linkR)
        """if linkR[:4]=="http":#bazı linklerde site ismi olmuyor onu kontrol edip eksikse tamamlayan bir yapı
            ic(linkR)
            link_name = link.text.replace("\n","")#.replace(" ","")
            print("{} : {}".format(link_name, linkR))

        elif linkR[:len(url)]!=url:
            ic(linkR)
            linkR = linkR.replace("/","",1)
            linkR = url + linkR
            link_name = link.text
            print("{} : {}".format(link_name, linkR))
        else:
            pass"""

        linkList.append(linkR)



def GetLink(link, firstList, secondList, control_Filter):
    global linkList
    global content_value
    global c_find
    c_find = False
    rq_con = rq.get(link)

    soup = BeautifulSoup(rq_con.content, 'html.parser')

    if secondList != [''] and firstList !=[''] and control_Filter != True :
        global c_parameters
        global content
        c_parameters = True

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
                            linkFinder_smart(links)

                            c_find = False
                            """
                            Bu döngü şu yüzden var: 2.filtrede 'filter2' değişkeninin 1'den fazla elemanında
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
        #iki parametre de boş bırakılırsa urldeki tüm linkleri bulur
        links = soup.find_all('a')
        print("\n      ______________________Links______________________\n")
        # ekstra filtre esnasında oluşan hatadan önce "links" yazısı çıkmaması için her koşula ayrı ayrı koydum
        linkFinder_smart(links)


    elif secondList != [''] and firstList !=[''] and control_Filter and c_parameters:

        #extraFilter sadece iki parametre de boş olmazsa kullnılabilir olacak
        community = content[content_value].contents[int(nums[0])]
        extraF = community.find_all(str(secondList[0]), {str(secondList[1]): str(secondList[2])})

        links = extraF[int(nums[1])].find_all("a")

        print("\n      ______________________Links______________________\n")
        # ekstra filtre esnasında oluşan hatadan önce "links" yazısı çıkmaması için her koşula ayrı ayrı koydum
        linkList = []
        linkFinder_smart(links)
        no_bug = False


    else:
        content = soup.find_all(str(firstList[0]), {str(firstList[1]): str(firstList[2])})
        print("\n      ______________________Links______________________\n")
        # ekstra filtre esnasında oluşan hatadan önce "links" yazısı çıkmaması için her koşula ayrı ayrı koydum
        for e in range(len(content)):
            for each in range(0, len(content[e].contents)):
                try:
                    links = content[e].contents[each].find_all("a")
                    linkFinder_smart(links)

                except AttributeError:
                    continue
                except IndexError:
                    continue

        content = soup.find_all(str(firstList[0]), {str(firstList[1]): str(firstList[2])})



    if len(linkList)==0:
        print("Bir hatadan ötürü linkler bulunamadı ya da hiç link yok!")
    else:
        print("\n___________________________________" + ("_" * len(str(len(linkList)))))  # sadece simetri için uğraştım
        print(f"________{len(linkList)} adet link bulundu!________")


url = input("url:")

if url[:4]=="http":

    parameter1 = input("parameter_1:")
    parameter2 = input("parameter_2:")
    firstList = parameter1.split(".")
    secondList = parameter2.split(".")
    GetLink(url, firstList, secondList, control_extraFilter)



    if len(linkList)!=0:
        question = input("\nDo you want use extraFilter? [y/n]:")

    else:
        question = str()

    while True:
        no_bug = True
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
    print("\n_________________________")
    print("______hatalı adres!______")
