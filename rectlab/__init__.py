from .engine import solve
from .verify import verify
from .families import select_from,rank_from

def select_witness(data,family,index):return select_from(solve(data),family,index)
def rank_witness(data,family,factors):return rank_from(solve(data),family,factors)
