
from libraro.tekstaPrilaborilo import TekstaPrilaborilo
from libraro.statiskaPrilaborilo import StatiskaPrilaborilo
from libraro.tradukilo import Tradukilo
from libraro.disigilo import Disigilo
import argparse

parser = argparse.ArgumentParser(description='Esperanto-dunianto .')
parser.add_argument('--enigo', help='enigo file', required=True)
parser.add_argument('--eligo', help='enigo file')
args = parser.parse_args()


disigilo = Disigilo()
tp = TekstaPrilaborilo()
sp = StatiskaPrilaborilo()
tradukilo = Tradukilo()

with open(args.enigo, encoding="utf-8") as sampleFile:
    sample = sampleFile.read()

from timeit import default_timer as timer
from datetime import timedelta
komTempo = timer()

disigilo.kuru(
    teksto=sample,
    iloj = [tp, sp, tradukilo]
)

finTempo = timer()
print(timedelta(seconds=finTempo-komTempo))




s = f'''
{sample}
-------------------------------------------------------------------
{tp.buffer}
-------------------------------------------------------------------
{tradukilo.teksto}
-------------------------------------------------------------------
{tradukilo.statistikoj}
{sp.statistikoj}
'''

if args.eligo is None:
    print(s)
else:
    with open(args.eligo, 'wt', encoding="utf-8") as f:
        f.write(s)

print('Done!')
