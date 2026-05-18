#!/usr/bin/env python3
import argparse,json
from coeffio import AC_COLUMNS,read_coeffs
def main():
 p=argparse.ArgumentParser(description="Analyze magnitude changes between cover and stego AC coefficients."); p.add_argument("--cover",required=True); p.add_argument("--stego",required=True); p.add_argument("--output",default="magnitude_report.json"); a=p.parse_args()
 _,cover=read_coeffs(a.cover); _,stego=read_coeffs(a.stego)
 if len(cover)!=len(stego): raise SystemExit("cover and stego row counts differ")
 changed=dec=inc=unch=before=after=dz=0
 for cr,sr in zip(cover,stego):
  for c in AC_COLUMNS:
   cv=int(cr[c]); sv=int(sr[c]); before+=abs(cv); after+=abs(sv)
   if cv!=sv:
    changed+=1
    if cv!=0 and sv==0: dz+=1
    if abs(sv)<abs(cv): dec+=1
    elif abs(sv)>abs(cv): inc+=1
    else: unch+=1
 rep={"total_changed":changed,"magnitude_decreased":dec,"magnitude_increased":inc,"magnitude_unchanged":unch,"total_abs_before":before,"total_abs_after":after,"abs_delta":after-before,"dangerous_zero_created":dz}
 open(a.output,"w").write(json.dumps(rep,indent=2,sort_keys=True)); print("magnitude decreased=%d increased=%d"%(dec,inc)); print("wrote %s"%a.output)
if __name__=="__main__": main()
