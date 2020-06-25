import codecs
import mojimoji
import jaconv
import json

ch0201_list = []
f = open('JIS0201.TXT', 'r')
for row in f:
    if row[0] != '#':
        code = row.split("\t")[0]
        char = row.split("\t")[1]
        ch0201_list.append({'code': int(code, 16), 'char': chr(int(char, 16))})
f.close()

ch0208_list = []
f = open('JIS0208.TXT', 'r')
for row in f:
    if row[0] != '#':
        code = row.split("\t")[1]
        char = row.split("\t")[2]
        ch0208_list.append({'code': int(code, 16), 'char': chr(int(char, 16))})
f.close()

conv_to_208 = {c['char']: c['code'] for c in ch0208_list}

convert_map = {}
for c in ch0201_list:
    cc = mojimoji.han_to_zen(c['char'])
    if cc in conv_to_208:
        convert_map[int(c['code'])] = int(conv_to_208[cc])
    else:
        pass
        
convert_map2 = {}
for c in ch0201_list:
    cc = mojimoji.han_to_zen(c['char'])
    cc = jaconv.kata2hira(cc)
    if cc in conv_to_208:
        convert_map2[int(c['code'])] = int(conv_to_208[cc])
    else:
        pass
        
with open('katakana_map.json', 'w') as f:
    json.dump(convert_map, f)

with open('hiragana_map.json', 'w') as f:
    json.dump(convert_map2, f)