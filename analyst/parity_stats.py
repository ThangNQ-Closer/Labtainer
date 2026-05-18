#!/usr/bin/env python3
import argparse,json
from coeffio import AC_COLUMNS,read_coeffs
def main():
 p=argparse.ArgumentParser(description="Compute parity distribution of nonzero AC coefficients."); p.add_argument("--infile",required=True); p.add_argument("--output",default="parity_report.json"); a=p.parse_args()
 _,rows=read_coeffs(a.infile); even=odd=zero=0
 for row in rows:
  for c in AC_COLUMNS:
   v=int(row[c])
   if v==0: zero+=1
   elif abs(v)%2==0: even+=1
   else: odd+=1
 total=even+odd
 rep={"nonzero_ac_total":total,"zero_ac_total":zero,"even":even,"odd":odd,"even_ratio":float(even)/float(total) if total else 0.0,"odd_ratio":float(odd)/float(total) if total else 0.0,"parity_gap":abs(even-odd)}
 open(a.output,"w").write(json.dumps(rep,indent=2,sort_keys=True)); print("even=%d odd=%d"%(even,odd)); print("wrote %s"%a.output)
if __name__=="__main__": main()
