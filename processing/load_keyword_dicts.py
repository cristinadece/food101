"""
Loaders for kw dictionaries and list
"""


def loadCategoryDict():
    """

    :return:
    """
    categoryDict = dict()
    # with open("./resources/categoriesWithSyn.txt") as g:
    with open("./resources/categoriesWithSyn.txt") as g:
        for line in g:
            # syn, categ = line.lower().replace("\r\n", "").split(",")
            # ht = "#" + syn.replace(" ", "")
            # categoryDict[syn] = categ
            # categoryDict[ht] = categ
            cat = line.lower().replace("\r\n", "")
            categoryDict[cat] = cat
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


    htCategoryList = list()
    with open("./resources/categories.txt") as g:
        for line in g:
            ht = "#" + line.lower().replace("\r\n", "").replace(" ", "")
            htCategoryList.append(ht)

    htString = ",".join(htList) + "," + ",".join(htCategoryList)
    return htString