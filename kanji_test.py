# encoding: utf-8
import xml.etree.ElementTree as ET
tree = ET.parse('kanjidic2.xml')
root = tree.getroot()
for kanji in root.findall('character'):

    try:
        grade = kanji[3].find('grade').text
        symbol = kanji.find('literal').text
        onReading = []
        kunReading = []
        print(symbol, grade)
        for child in kanji.find('reading_meaning')[0]:
            if child.tag == "meaning" and not (child.attrib):
                print("meaning: ", child.text)
            if child.attrib["r_type"] == "ja_on":
                print("on: ", child.text)
            if child.attrib["r_type"] == "ja_kun":
                print("kun: ", child.text)
    except:
        pass
    #nesting nanori in separate try clause, some kanji might not have

    try:
        for child in kanji.find('reading_meaning'):
            if child.tag == "nanori":
                print("nanori", child.text)
    except:
        pass