"""
Loaders for kw dictionaries and list
"""
import codecs


def loadCategoryDict():
    """

    :return:
    """
    categoryDict = dict()
    with codecs.open("./resources/categoriesWithSyn.txt", "r", "utf-8") as g:
        for line in g:
            syn, categ = line.lower().replace("\r\n", "").split(",")
            ht = "#" + syn.replace(" ", "")
            categoryDict[syn] = categ.strip().replace(" ", "_")
            categoryDict[ht] = categ.strip().replace(" ", "_")
    return categoryDict


def getStreamFilterKeywords():
    """
    from the kw.txt and from categories.txt - with some processing to it
    :return: a string a keywords separated by comma
    """
    htList = list()
    with open("./resources/kw.txt") as f:
        for line in f:
            ht = line.replace("\n", "")
            htList.append(ht)
    htList.append("#foodsigir2017")

    htCategoryList = list()
    with open("./resources/categories.txt") as g:
        for line in g:
            ht = "#" + line.lower().replace("\r\n", "").replace(" ", "")
            htCategoryList.append(ht)

    htString = ",".join(htList) + "," + ",".join(htCategoryList)
    return htString