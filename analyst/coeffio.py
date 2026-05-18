#!/usr/bin/env python3
import csv
META_COLUMNS=["frame","block_id","plane","tx_size","ac_energy","nonzero_ac"]
COEFF_COLUMNS=["c%d"%i for i in range(16)]
AC_COLUMNS=["c%d"%i for i in range(1,16)]
CSV_COLUMNS=META_COLUMNS+COEFF_COLUMNS
def sign(v): return 1 if v>0 else -1
def read_coeffs(path):
 rows=[]
 with open(path,"r",newline="") as fh:
  r=csv.DictReader(fh); fields=r.fieldnames or []
  for row in r:
   item={}
   for k,v in row.items(): item[k]=v if k in ("plane","tx_size") else (int(v) if k in CSV_COLUMNS else v)
   rows.append(item)
 return fields,rows
def write_coeffs(path,rows):
 with open(path,"w",newline="") as fh:
  wr=csv.DictWriter(fh,fieldnames=CSV_COLUMNS); wr.writeheader()
  for row in rows: wr.writerow(dict((c,row[c]) for c in CSV_COLUMNS))
def recalc_row(row):
 e=0; n=0
 for c in AC_COLUMNS:
  v=int(row[c]); e+=abs(v); n+=1 if v!=0 else 0
 row["ac_energy"]=e; row["nonzero_ac"]=n
def message_to_bits(msg):
 data=msg.encode("utf-8"); bits=[]; L=len(data)
 for sh in range(31,-1,-1): bits.append((L>>sh)&1)
 for b in data:
  for sh in range(7,-1,-1): bits.append((b>>sh)&1)
 return bits
def bits_to_message(bits):
 if len(bits)<32: return "",0,False
 L=0
 for b in bits[:32]: L=(L<<1)|int(b)
 need=32+L*8
 if len(bits)<need: return "",L,False
 out=[]; off=32
 for i in range(L):
  v=0
  for b in bits[off:off+8]: v=(v<<1)|int(b)
  out.append(v); off+=8
 try: return bytes(bytearray(out)).decode("utf-8"),L,True
 except UnicodeDecodeError: return "",L,False
def eligible(v,min_abs):
 v=int(v)
 return v!=0 and abs(v)>int(min_abs) and abs(v)>1
