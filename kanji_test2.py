# encoding: utf-8
import xml.etree.ElementTree as ET
from collections import OrderedDict

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
print(masterDictionary)
print(masterDictionary["木"])