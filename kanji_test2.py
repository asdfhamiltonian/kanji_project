# encoding: utf-8
import xml.etree.ElementTree as ET
from collections import OrderedDict
from math import sqrt

tree = ET.parse('kanjidic2.xml')
root = tree.getroot()

masterDictionary = OrderedDict()

for kanji in root.findall('character'):
    if kanji[3].find('grade') is not None:
        grade = int(kanji[3].find('grade').text)
        symbol = kanji.find('literal').text
        try:
            freq = kanji[3].find('freq').text
        except:
            freq = "NA"

        try:
            jlpt = kanji[3].find('jlpt').text
        except:
            jlpt = "NA"

        tempdict = OrderedDict()
        tempdict["grade"] = grade
        tempdict["jlpt"] = jlpt
        tempdict["freq"] = freq

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

print(len(masterDictionary))

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

def avg(x):
    return sum(x)/len(x)

def variance(x):
    x_bar = avg(x)
    list = [(x_i - x_bar)**2 for x_i in x]
    return sum(list)/(len(list) - 1)

def sd(x):
    return sqrt(variance(x))

print("Average kanji grade level:", avg(charArray))
print("Variance:", variance(charArray))
print("Standard Deviation:", sd(charArray))
print(masterDictionary["祢"])