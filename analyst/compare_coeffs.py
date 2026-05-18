#!/usr/bin/env python3
import argparse,json
from coeffio import AC_COLUMNS,read_coeffs
def main():
 p=argparse.ArgumentParser(description="Compare cover and stego coefficient CSV files."); p.add_argument("--cover",required=True); p.add_argument("--stego",required=True); p.add_argument("--output",default="compare_report.json"); a=p.parse_args()
 _,cover=read_coeffs(a.cover); _,stego=read_coeffs(a.stego)
 if len(cover)!=len(stego): raise SystemExit("cover and stego row counts differ")
 total=changed=dc=z2n=n2z=plus=minus=other=0
 for cr,sr in zip(cover,stego):
  if int(cr["c0"])!=int(sr["c0"]): dc+=1
  for c in AC_COLUMNS:
   cv=int(cr[c]); sv=int(sr[c]); total+=1
   if cv!=sv:
    changed+=1; d=sv-cv
    if cv==0 and sv!=0: z2n+=1
    if cv!=0 and sv==0: n2z+=1
    if d==1: plus+=1
    elif d==-1: minus+=1
    else: other+=1
 rep={"total_ac":total,"changed_ac":changed,"changed_ratio":float(changed)/float(total) if total else 0.0,"dc_changed":dc,"zero_to_nonzero":z2n,"nonzero_to_zero":n2z,"plus_one_changes":plus,"minus_one_changes":minus,"other_changes":other}
 open(a.output,"w").write(json.dumps(rep,indent=2,sort_keys=True)); print("changed AC coefficients: %d"%changed); print("wrote %s"%a.output)
if __name__=="__main__": main()
