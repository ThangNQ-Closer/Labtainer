#!/usr/bin/env python3
import argparse,random
from coeffio import AC_COLUMNS,write_coeffs,recalc_row
def sample(r):
 if r.random()<0.24: return 0
 m=r.choice([1,1,2,2,3,3,4,5,6,8,10,12])
 return m if r.random()<0.5 else -m
def main():
 p=argparse.ArgumentParser(description="Generate VP9-style quantized transform coefficient CSV data.")
 p.add_argument("--output",default="cover_coeffs.csv"); p.add_argument("--frames",type=int,default=30); p.add_argument("--blocks-per-frame",type=int,default=120); p.add_argument("--seed",type=int,default=20260518)
 a=p.parse_args(); r=random.Random(a.seed); rows=[]; bid=0
 for fr in range(a.frames):
  for _ in range(a.blocks_per_frame):
   row={"frame":fr,"block_id":bid,"plane":r.choice(["Y","Y","Y","U","V"]),"tx_size":r.choice(["4x4","8x8","16x16"]),"c0":r.choice([-18,-12,-8,-5,5,8,12,18])}
   for c in AC_COLUMNS: row[c]=sample(r)
   recalc_row(row); rows.append(row); bid+=1
 write_coeffs(a.output,rows); print("wrote %s rows to %s"%(len(rows),a.output)); print("c0 is DC and c1..c15 are AC coefficients")
if __name__=="__main__": main()
