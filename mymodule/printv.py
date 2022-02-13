import sys
def printv(*value,sep=' ',end='\n',write=False,file=sys.stdout,flush=False) ->str:
    if write == True:
        print(value,sep=sep,end=end,file=file,flush=flush)
    rv = ''
    for i in value:
        rv = rv + str(i) + sep
    rv = rv + end
    return rv