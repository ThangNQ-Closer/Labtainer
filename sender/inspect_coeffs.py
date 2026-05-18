#!/usr/bin/env python3
import argparse,json
from coeffio import CSV_COLUMNS,AC_COLUMNS,read_coeffs
def main():
 p=argparse.ArgumentParser(description="Inspect VP9-style coefficient CSV structure."); p.add_argument("--input",default="cover_coeffs.csv"); p.add_argument("--output",default="coeff_info.json"); a=p.parse_args()
 fields,rows=read_coeffs(a.input); zero=0; non=0; mn=None; mx=0
 for row in rows:
  for c in AC_COLUMNS:
   v=int(row[c])
   if v==0: zero+=1
   else:
    non+=1; av=abs(v); mn=av if mn is None or av<mn else mn; mx=max(mx,av)
 info={"inspected":True,"row_count":len(rows),"columns":fields,"required_columns_present":all(c in fields for c in CSV_COLUMNS),"dc_column":"c0","ac_columns":AC_COLUMNS,"zero_ac_total":zero,"nonzero_ac_total":non,"min_nonzero_abs_ac":mn or 0,"max_abs_ac":mx,"embedding_note":"Directed parity uses nonzero AC above min_abs; c0 remains unchanged."}
 open(a.output,"w").write(json.dumps(info,indent=2,sort_keys=True)); print("wrote %s"%a.output); print("DC coefficient: c0"); print("AC coefficients: c1..c15")
if __name__=="__main__": main()
