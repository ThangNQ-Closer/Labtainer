#!/usr/bin/env python3
import argparse,json
from coeffio import AC_COLUMNS,read_coeffs,bits_to_message,eligible
def main():
 p=argparse.ArgumentParser(description="Extract a directed-parity embedded message."); p.add_argument("--infile",required=True); p.add_argument("--output",default="extract_report.json"); p.add_argument("--min-abs",type=int,default=2); a=p.parse_args()
 fields,rows=read_coeffs(a.infile); bits=[]; L=None; need=None
 for row in rows:
  for c in AC_COLUMNS:
   v=int(row[c])
   if not eligible(v,a.min_abs): continue
   bits.append(abs(v)%2)
   if len(bits)==32 and L is None:
    L=0
    for b in bits: L=(L<<1)|int(b)
    need=32+L*8
   if need is not None and len(bits)>=need: break
  if need is not None and len(bits)>=need: break
 msg,L,ok=bits_to_message(bits); used=len(bits if need is None else bits[:need])
 rep={"extracted_message":msg,"extracted_bits":used,"payload_length":L,"success":bool(ok),"min_abs":a.min_abs}
 open(a.output,"w").write(json.dumps(rep,indent=2,sort_keys=True)); print("extracted message: %s"%msg); print("wrote %s"%a.output)
if __name__=="__main__": main()
