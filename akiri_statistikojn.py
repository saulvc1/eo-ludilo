
from libraro.statiskaPrilaborilo import StatiskaPrilaborilo
from libraro.disigilo import Disigilo

import argparse
parser = argparse.ArgumentParser(description='Kreinto de statistikoj.')
parser.add_argument('--dosierujo', help='dosierujo kun esperanta literaturo', required=False)
args = parser.parse_args()
dosierujo = './datoj/Gutenberg' if args.dosierujo is None else args.dosierujo



disigilo = Disigilo()
spA = StatiskaPrilaborilo()
sp1 = None
sp2 = None

from pathlib import Path

alineo = ''
count_ln = 0
total_ln = 0
def aktualigiStatiskojn():
    global sp1, sp2, alineo, count_ln, total_ln
    disigilo.kuru(teksto=alineo, iloj=[sp2])

    if sp2.konProporcio() >= 0.65:
        sp1.update(sp2)
        count_ln += 1
    total_ln += 1


for txtPath in Path('./datoj/Gutenberg').glob('*.txt'):
    print(txtPath, end=' ')
    with txtPath.open('rt', encoding='utf-8') as txt:
        count_ln = 0
        total_ln = 0
        sp1 = StatiskaPrilaborilo()

        for linio in txt:
            if linio.upper().lstrip().startswith('*** START OF'):
                break

        for linio in txt:
            linio = linio.strip()
            if linio.upper().startswith('*** END OF'):
                break

            # La alineo finigxis.
            if len(linio) == 0:
                if sp2 is not None:    
                    aktualigiStatiskojn()
                    alineo = ''
                    sp2 = None
            else:
                if sp2 is None:
                    sp2 = StatiskaPrilaborilo()
                alineo += linio

        if sp2 is not None:
            aktualigiStatiskojn()
        if total_ln == 0:
            print('0%')
        else:
            t = 100 * count_ln / total_ln
            if t >= 70:
                spA.update(sp1)
                print('{0:.2f}% konataj vortoj --> bone'.format(t))
            else:
                print('{0:.2f}% konataj vortoj'.format(t))

def konserviKielCSV(irejo, vortaro):
    with open(irejo, 'wt', encoding='utf-8') as dosiero:
        dosiero.write('vorto,frekvenco,longeco\n')
        for sx, frekvenco in sorted(vortaro.items(), key=lambda x:x[1], reverse=True):
            dosiero.write(f'{sx},{frekvenco},{len(sx)}\n')

from datetime import datetime
nun = datetime.now().strftime("%Y_%d_%m__%H_%M_%S")

konserviKielCSV(f'../Rezultoj/konataj_radikoj_{nun}.csv',   spA.konataro)
konserviKielCSV(f'../Rezultoj/nekonataj_radikoj_{nun}.csv', spA.nekonataro)
konserviKielCSV(f'../Rezultoj/konataj_vortoj_{nun}.csv',    spA.vortaro)