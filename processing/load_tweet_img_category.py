"""

"""
import codecs


def loadCategoryDict(filename):
    """

    :return:
    """
    tweetImgCategoryDict = dict()
    with codecs.open(filename, "r", "utf-8") as g:
        print g.readline()
        for line in g:
            lineData = line.lower().replace("\n", "").split("\t")
            if lineData[1] != "unknown":
                tweetImgCategoryDict[long(lineData[0])] = tuple((lineData[2], float(lineData[3])))
    return tweetImgCategoryDict

if __name__ == '__main__':
    dik = loadCategoryDict("/Users/muntean/Downloads/twitter.report/twitter.03.report.tsv")
    print len(dik)
    print dik[840194355319209984]