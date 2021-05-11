
from libraro.disigilo import Disigilo
disigilo = Disigilo()

morfemoj = [k for k,v in disigilo.radikaro.items() if len(v)==1]

def disigiVorton(vorto):
    l = []

    if vorto == '':
        return l

    for morfemo in morfemoj:
        #if morfemo == 'ne':
        #    breakpoint()
        if vorto.startswith(morfemo):
            cetero = vorto[len(morfemo):]
            if len(cetero) == 1:
                l.append([morfemo, [cetero]])
                break
            elif len(cetero) > 1:
                ll = disigiVorton(cetero)
                if len(ll) >  0:
                    l.append([morfemo, ll])
    if len(l) == 0:
        if vorto[0] in 'aeoi':
            ll = disigiVorton(vorto[1:])
            if len(ll) > 0:
                l.append([vorto[0], ll])
    return l
            

from pprint import pprint
# dis = disigiVorton('nevidebla')
# pprint(dis)

disigoj = []

def listi(l, s=None):
    global disigoj
    if len(l) == 0:
        disigoj.append(s)
        return

    if len(l) == 1 and type(l[0]) == str:
        disigoj.append(s + '-' + l[0])
        return

    ss = [] if s is None else s
    for x in l:
        if type(x) == str:
            if len(ss) == 0:
                ss = x
            else:
                ss += f'-{x}'
        else:
            listi(x, ss)

'''
with open('nepermesataj.txt', 'wt', encoding='utf-8') as dosiero:
    for vorto in disigilo.vortaro.keys():
        disigoj = []
        listi(disigiVorton(vorto))
        
        if len(disigoj) > 1:
            cxio = ', '.join(disigoj)
            dosiero.write(f'{vorto}: {len(disigoj)}: {cxio}\n')
'''

lingvoj = []
# from collections import defaultdict
# tablo = defaultdict(dict)
vortaro = {}

import re
with open('datoj/vortaro/Etimologioj.txt', 'rt', encoding='utf-8') as dosiero:
    # Ekz:
    # acida = Fre. acide, Ita. acido, Eng. acid, Lat. acidus
    # --> vortaro['acid'] = ('acida', {'Fre': 'acide', 'Ita': 'acido', 'Eng': 'acid', 'Lat': 'acidus'})
    for line in dosiero:
        line = line.strip()
        if len(line) > 1:
            try:
                vorto, etimologio = re.split('\s*=\s*', line.replace('[calque of', '=').replace('[back-formation from', '=').replace(']',''), 1)
            except ValueError:
                breakpoint()
            etimologio = [re.split('\.\s*', x, 1) for x in re.split(',\s*', etimologio)]
            etimologio = {x[0]:x[1] for x in etimologio if len(x) == 2}

            vortaro[vorto[:-1]] = (vorto, etimologio, 'eo')
            for lingvo in etimologio.keys():
                if lingvo not in lingvoj:
                    lingvoj.append(lingvo)
        #if line.startswith('acid'):
        #    breakpoint()


import pathlib
def saviTabulo(dosieraNomo, vortaro):
    p = pathlib.Path('../Rezultoj/Statistikoj/') / dosieraNomo
    lingvoj.sort()
    with p.open('wt', encoding='utf-8') as tab:
        tab.write('Lingvo,Radiko,Vorto,' + ','.join(lingvoj) + '\n')
        for k, (x,y,z) in vortaro.items():
            #if k == 'abi':
            #    breakpoint()
            d = {lingvo:'' for lingvo in lingvoj}
            for lingvo, vorto in y.items():
                d[lingvo] = vorto

            row = f'{z},{k},{x}'
            for lingvo in lingvoj:
                row += f',{d[lingvo]}'
            tab.write(row + '\n')

saviTabulo('vortaro_eo.csv', vortaro)

if 'nekonata' not in lingvoj:
    lingvoj.append('nekonata')

forigataj = []

import csv
with open('./datoj/vortaro/Wokitabo.csv') as csvDosiero:
    
    for row in csv.reader(csvDosiero, delimiter=','):
        
        for x in ['retroskribo', 'simpligita']:
            if x in row[2]:
                row[2] = x

        #if 'ar (' in row[2]:
        #    breakpoint()
        # print("@", row)

        if row[2] == 'etimologio':
            continue
        if row == ['', '', '']:
            continue
        #print('--->', row)

        if len(row) <= 1:
            continue
        elif len(row) == 2:
            elDunianto, elEsperanto = row
            origino = {}
        else:
            elDunianto, elEsperanto, origino = row
            elDunianto = elDunianto.lower()
            elEsperanto = elEsperanto.lower()

            origino = re.sub('\(.+?\)', '', origino)
            origino = origino.replace('"', '').replace('+', ',').replace(';', ',').replace('[calque of', ':')
            #print('#####', origino)
            if origino == '':
                origino = {}
            else:
                origino = [x.strip().split(':') for x in origino.split(',') if x != '']
                #print('#####->', origino)
                origino = [x if len(x) >= 2 else [x[0],'nekonata'] for x in origino]
                #print('#####--->', origino)
                origino = {k.strip():v.strip() for k,v in origino}
                # print('#####---->', origino)

        #if '/' in elEsperanto:
        #    continue
        if elEsperanto == elDunianto:
            continue
        if elEsperanto in vortaro:
            #print(f'{elEsperanto} removed.')
            del vortaro[elEsperanto]
            forigataj.append(elEsperanto)

        etimologio = {}
        for k, v in origino.items():
            if '/' in k:
                for x in k.split('/'):
                    etimologio[x] = v
            else:
                etimologio[k] = v


        if '/' not in  elDunianto:
            vortaro[elDunianto] = (elDunianto, etimologio, 'dun')
            for lingvo in etimologio.keys():
                if lingvo not in lingvoj:
                    lingvoj.append(lingvo)
        else:
            for x in elDunianto.split('/'):
                if x not in vortaro:
                    vortaro[x] = (x, {'nekonata':'---'}, 'dun')

        
        

saviTabulo('vortaro_dun.csv', vortaro)


print(f'{len(forigataj)} removed')
#ciujRadikoj = 

# print(disigoj)
