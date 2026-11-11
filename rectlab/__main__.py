import argparse,json,sys
from .engine import solve
from .families import select_from,rank_from
from .verify import verify
from .schema import loads

def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['solve','verify','select','rank']);p.add_argument('path',nargs='?',default='-');p.add_argument('--family',default='cover',choices=['cover','maximal_cover','partition']);p.add_argument('--index',default='0');p.add_argument('--factors',default='[]');a=p.parse_args()
    try:
        text=sys.stdin.read() if a.path=='-' else open(a.path).read();x=loads(text)
        if a.command=='solve':out=solve(x)
        elif a.command=='verify':out={'valid':verify(x)}
        elif a.command=='select':out={'family':a.family,'index':a.index,'factors':select_from(solve(x),a.family,a.index)}
        else:out={'family':a.family,'index':rank_from(solve(x),a.family,loads(a.factors))}
        print(json.dumps(out,sort_keys=True,separators=(',',':')))
    except (ValueError,KeyError,TypeError,OSError) as e:print(str(e),file=sys.stderr);return 2
    return 0
if __name__=='__main__':sys.exit(main())
