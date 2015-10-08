# encoding: utf-8
import xml.etree.ElementTree as ET
tree = ET.parse('kanjidic2.xml')
root = tree.getroot()
for kanji in root.findall('character'):

    try:
        grade = kanji[3].find('grade').text
        symbol = kanji.find('literal').text
        try:
            freq = kanji[3].find('freq').text
        except:
            freq = "NA"
        try:
            jlpt = kanji[3].find('jlpt').text
        except:
            jlpt = "NA"

        print(symbol, "grade: ", grade, "jlpt: ", jlpt, "freq: ", freq)

        for node in kanji.find('dic_number'):
            if node.attrib["dr_type"] == "nelson_c":
                print("Nelson: ", node.text)
            elif node.attrib["dr_type"] == "oneill_kk":
                print("O'Neill: ", node.text)

        for child in kanji.find('reading_meaning')[0]:
            #python seems to behave badly with series of if statements,
            #preferred this to be set up as if, elif, elif, else
            if child.tag == "meaning" and (not child.attrib):
                print("meaning: ", child.text)
            elif child.attrib["r_type"] == "ja_on":
                print("on: ", child.text)
            elif child.attrib["r_type"] == "ja_kun":
                print("kun: ", child.text)
            else:
                pass

    except:
        pass
    #nesting nanori in separate try clause, some kanji might not have

    try:
        for child in kanji.find('reading_meaning'):
            if child.tag == "nanori":
                print("nanori", child.text)
            else:
                pass
    except:
        pass