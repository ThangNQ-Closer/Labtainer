#!/usr/bin/env python3
import argparse,json
from coeffio import AC_COLUMNS,read_coeffs,write_coeffs,recalc_row,message_to_bits,eligible,sign
def main():
 p=argparse.ArgumentParser(description="Embed by directed parity coding in VP9-style AC coefficients."); p.add_argument("--infile",required=True); p.add_argument("--outfile",required=True); p.add_argument("--message",required=True); p.add_argument("--min-abs",type=int,default=2); a=p.parse_args()
 fields,rows=read_coeffs(a.infile); bits=message_to_bits(a.message); idx=0; changed=0; cand=0; skip0=0; skips=0; dc0=[r["c0"] for r in rows]
 for row in rows:
  if idx>=len(bits): break
  for c in AC_COLUMNS:
   if idx>=len(bits): break
   v=int(row[c])
   if v==0: skip0+=1; continue
   if not eligible(v,a.min_abs): skips+=1; continue
   cand+=1; target=bits[idx]
   if abs(v)%2!=target:
    nv=v-sign(v)
    if nv==0 or abs(nv)<=a.min_abs:
     nv=v+sign(v)
    row[c]=nv; changed+=1
   idx+=1
  recalc_row(row)
 if idx<len(bits): raise SystemExit("not enough eligible AC coefficients: embedded %d of %d bits"%(idx,len(bits)))
 for row in rows: recalc_row(row)
 write_coeffs(a.outfile,rows); dc1=[r["c0"] for r in rows]
 rep={"algorithm":"directed_parity","message":a.message,"payload_length":len(a.message.encode("utf-8")),"embedded_bits":idx,"changed_ac":changed,"candidates_used":cand,"skipped_zero":skip0,"skipped_small_or_min_abs":skips,"min_abs":a.min_abs,"dc_changed":0 if dc0==dc1 else 1,"zero_to_nonzero":0,"direction_rule":"mismatched parity moves coefficient one step toward zero"}
 open("embed_report.json","w").write(json.dumps(rep,indent=2,sort_keys=True)); print("embedded %d bits into %s"%(idx,a.outfile)); print("changed AC coefficients: %d"%changed)
if __name__=="__main__": main()
