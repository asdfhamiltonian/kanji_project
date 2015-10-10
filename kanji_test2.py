# encoding: utf-8
'''
This package uses the EDICT and KANJIDIC dictionary files. (see http://www.csse.monash.edu.au/~jwb/kanjidic.html)
These files are the property of the Electronic Dictionary Research and Development Group,
and are used in conformance with the Group's licence.
'''
import os.path
import pickle
import xml.etree.ElementTree as ET
from collections import OrderedDict
from math import sqrt
import matplotlib.pyplot as plt

tree = ET.parse('kanjidic2.xml')
root = tree.getroot()
masterDictionary = OrderedDict()

if not os.path.isfile("kanjiPickle.p"):
    for kanji in root.findall('character'):
        if kanji[3].find('grade') is not None:
            tempdict = OrderedDict()
            tempdict["grade"] = int(kanji[3].find('grade').text)
            symbol = kanji.find('literal').text
            try:
                tempdict["freq"] = int(kanji[3].find('freq').text)
            except:
                tempdict["freq"] = "NA"

            try:
                tempdict["jlpt"] = int(kanji[3].find('jlpt').text)
            except:
                tempdict["jlpt"] = "NA"

            for node in kanji.find('dic_number'):
                if node.attrib["dr_type"] == "nelson_c":
                    tempdict["Nelson"] = node.text
                elif node.attrib["dr_type"] == "oneill_kk":
                    tempdict["O'Neill"] = node.text
                else:
                    pass

            meaning = []
            onyomi = []
            kunyomi = []

            for child in kanji.find('reading_meaning')[0]:
                #python seems to behave badly with series of if statements,
                #preferred this to be set up as if, elif, elif, else
                if (child.tag == "meaning") and (child.attrib == {}):
                    meaning.append(child.text)
                elif ("r_type" in child.attrib) and (child.attrib["r_type"] == "ja_on"):
                    onyomi.append(child.text)
                elif ("r_type" in child.attrib) and (child.attrib["r_type"] == "ja_kun"):
                    kunyomi.append(child.text)
                else:
                    pass

            nanori = []
            for child in kanji.find('reading_meaning'):
                if child.tag == "nanori":
                    nanori.append(child.text)
                else:
                    pass

            tempdict["ja_on"] = onyomi
            tempdict["ja_kun"] = kunyomi
            tempdict["meaning"] = meaning
            tempdict["nanori"] = nanori

            masterDictionary[symbol] = tempdict
    pickle.dump(masterDictionary, open("kanjiPickle.p", "wb"))
else:
    '''
    Getting this to work after unpickling was confusing. It seems that pickle/unpickle
    returns strings in a different format than Python natively works with. Some of my logic
    compared the string "NA" with and "NA" from a dictionary entry. However, I used the "is not"
    operator, which it turns out tests whether objects are the exact same thing. != works the same
    way but is testing for value. The code unpickles now that I changed out the "is nots"
    for !='s. Whew! See: http://stackoverflow.com/questions/4485180/python-is-not-operator
    Took several hours to debug this.
    '''
    masterDictionary = pickle.load(open("kanjiPickle.p", "rb"))

print(len(masterDictionary), "\n")

#Will use the dictionary to try grade-level analysis on the
#Iroha poem written in Man'yogana
#Thinking about turning this into a feature for text analysis


iroha = "以 呂 波 耳 本 部 止千 利 奴 流 乎 和 加餘 多 連 曽 津 祢 那良 牟 有 為 能 於 久耶 万 計 不 己 衣 天阿 佐 伎 喩 女 美 之恵 比 毛 勢 須"
iroha = iroha.replace(" ","")
print(iroha)
charArray = []
for char in iroha:
    if char in masterDictionary:
        grade = int(masterDictionary[char]["grade"])
        charArray.append(grade)
    else:
        pass
print(charArray)

#may want to just use numpy in the future.
def avg(x):
    return sum(x)/len(x)

def variance(x):
    x_bar = avg(x)
    squareDiffList = [(x_i - x_bar)**2 for x_i in x]
    return sum(squareDiffList)/(len(squareDiffList) - 1)

def sd(x):
    return sqrt(variance(x))

def correlation(tuplist):
    '''
    solves for the correlation of a list of tupples
    '''
    x_list = [item[0] for item in tuplist]
    y_list = [item[1] for item in tuplist]
    x_bar = avg(x_list)
    s_x = sd(x_list)
    y_bar = avg(y_list)
    s_y = sd(y_list)
    n = len(tuplist)
    numerator_list = [(item[0] - x_bar) * (item[1] - y_bar) for item in tuplist]
    r = sum(numerator_list)/((n-1) * s_x * s_y)
    return r

print("Average kanji grade level:", avg(charArray))
print("Variance:", variance(charArray))
print("Standard Deviation:", sd(charArray))
print(masterDictionary["祢"], "\n")

#calculating correlation between jlpt, grade level
jlptGradeList = []
for char in masterDictionary:
    if masterDictionary[char]["jlpt"] != "NA":
        newtup = int(masterDictionary[char]["jlpt"]), masterDictionary[char]["grade"]
        jlptGradeList.append(newtup)

x0, y0 = zip(*jlptGradeList)
e = plt.figure(0)
plt.scatter(x0,y0)
plt.xlabel("JLPT level")
plt.ylabel("Grade")
plt.title("Graph of Grade vs. JLPT level for Kanji with both attributes")
e.show()

r = correlation(jlptGradeList)
print("JLPT, grade correlation: ", r)
print("R^2: ", r**2, "\n")

#correlation between grade level, frequency ranking
gradeFrequency = []
for char in masterDictionary:
    if masterDictionary[char]["freq"] != "NA":
        newtup = int(masterDictionary[char]["grade"]), int(masterDictionary[char]["freq"])
        gradeFrequency.append(newtup)

x1, y1 = zip(*gradeFrequency)
plt.scatter(x1,y1)
plt.xlabel("Grade Level")
plt.ylabel("Character Frequency Ranking")
plt.title("Graph of Grade Level vs. Frequency Ranking for Kanji Characters with Both Values")
plt.show()

r = correlation(gradeFrequency)
print("grade, frequncy ranking correlation: ", r)
print("R^2: ", r**2, "\n")

#correlation between Nelson index, O'Neill index (shouldn't necessarily be correlated):
OneillNelsonList = []
for char in masterDictionary:
    if ("O'Neill" in masterDictionary[char]) and ("Nelson" in masterDictionary[char]):
        newtup = int(masterDictionary[char]["O'Neill"]), int(masterDictionary[char]["Nelson"])
        OneillNelsonList.append(newtup)

x2, y2 = zip(*OneillNelsonList)
plt.scatter(x2,y2)
plt.xlabel("O'Neill Index")
plt.ylabel("Nelson Index")
plt.title("Graph of Nelson Index vs. O'Neill Index for Shared Kanji")
plt.show()


r = correlation(OneillNelsonList)
print("O'Neil index, Nelson index correlation: ", r)
print("R^2: ", r**2, "\n")



'''
JLPT, grade correlation:  -0.8085980116337447
R^2:  0.6538307444180455

grade, frequncy ranking correlation:  0.740460651262813
R^2:  0.5482819760685492

O'Neil index, Nelson index correlation:  0.06092591580369111
R^2:  0.003711967216518458
'''