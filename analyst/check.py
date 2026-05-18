#!/usr/bin/env python3
import argparse,csv,json,os,sys
SECRET="DEFENSIVE-LAB-PAYLOAD-ONLY"
CHECKS=["coefficients_created","coefficients_inspected","parity_embedding_completed","message_extracted","magnitude_analyzed","labtainer_outputs_ready"]
AC_COLUMNS=["c%d"%i for i in range(1,16)]
COEFF_COLUMNS=["c0"]+AC_COLUMNS
CSV_COLUMNS=["frame","block_id","plane","tx_size","ac_energy","nonzero_ac"]+COEFF_COLUMNS
def load_json(p):
 with open(p,"r") as f: return json.load(f)
def read_csv(p):
 with open(p,"r",newline="") as f:
  r=csv.DictReader(f); rows=[]
  for row in r:
   item={}
   for k,v in row.items(): item[k]=v if k in ("plane","tx_size") else (int(v) if k in CSV_COLUMNS else v)
   rows.append(item)
  return r.fieldnames or [],rows
def dirs(base):
 out=[]
 for d in [base,os.getcwd(),os.path.expanduser("~"),"/shared"]:
  for x in [d,os.path.join(d,"sender"),os.path.join(d,"analyst"),os.path.join(d,"shared")]:
   if x not in out: out.append(x)
 return out
def find_file(base,name):
 for d in dirs(base):
  p=os.path.join(d,name)
  if os.path.exists(p): return p
 for root in [base,os.path.expanduser("~"),"/shared"]:
  if not os.path.isdir(root): continue
  for cur,subs,files in os.walk(root):
   if name in files: return os.path.join(cur,name)
   if cur[len(root):].count(os.sep)>=3: subs[:]=[]
 return None
def diff_summary(cover,stego):
 if len(cover)!=len(stego): return None
 changed=dc=z2n=n2z=0
 for cr,sr in zip(cover,stego):
  if cr["c0"]!=sr["c0"]: dc+=1
  for c in AC_COLUMNS:
   cv=cr[c]; sv=sr[c]
   if cv!=sv:
    changed+=1
    if cv==0 and sv!=0: z2n+=1
    if cv!=0 and sv==0: n2z+=1
 return {"changed":changed,"dc_changed":dc,"zero_to_nonzero":z2n,"nonzero_to_zero":n2z}
def ratio(v): return isinstance(v,(int,float)) and 0.0<=float(v)<=1.0
def evaluate(base):
 paths=dict((k,find_file(base,n)) for k,n in [("cover","cover_coeffs.csv"),("stego","stego_parity.csv"),("coeff_info","coeff_info.json"),("embed","embed_report.json"),("extract","extract_report.json"),("compare","compare_report.json"),("parity","parity_report.json"),("magnitude","magnitude_report.json")])
 res=dict((n,False) for n in CHECKS); cover=[]; stego=[]; diff=None
 if paths["cover"]:
  fields,cover=read_csv(paths["cover"]); res["coefficients_created"]=len(cover)>0 and all(c in fields for c in CSV_COLUMNS)
 if paths["coeff_info"]:
  info=load_json(paths["coeff_info"]); res["coefficients_inspected"]=bool(info.get("inspected")) and info.get("dc_column")=="c0" and info.get("ac_columns")==AC_COLUMNS and info.get("nonzero_ac_total",0)>0
 if paths["stego"] and cover:
  fields,stego=read_csv(paths["stego"]); diff=diff_summary(cover,stego)
 if paths["embed"] and diff is not None:
  emb=load_json(paths["embed"]); res["parity_embedding_completed"]=emb.get("embedded_bits",0)>0 and emb.get("dc_changed",1)==0 and diff["changed"]>0 and diff["dc_changed"]==0 and diff["zero_to_nonzero"]==0 and diff["nonzero_to_zero"]==0
 if paths["extract"]:
  ex=load_json(paths["extract"]); res["message_extracted"]=ex.get("extracted_message")==SECRET and ex.get("payload_length")==len(SECRET.encode("utf-8")) and ex.get("extracted_bits",0)>0 and bool(ex.get("success"))
 if paths["compare"] and paths["parity"] and paths["magnitude"] and diff is not None:
  comp=load_json(paths["compare"]); par=load_json(paths["parity"]); mag=load_json(paths["magnitude"])
  comp_ok=comp.get("changed_ac",0)>0 and comp.get("dc_changed",1)==0 and comp.get("zero_to_nonzero",-1)==0 and comp.get("nonzero_to_zero",-1)==0 and diff["changed"]>0
  par_ok=ratio(par.get("even_ratio")) and ratio(par.get("odd_ratio"))
  mag_ok=mag.get("total_changed",0)>0 and mag.get("dangerous_zero_created",-1)==0 and mag.get("magnitude_decreased",-1)>=mag.get("magnitude_increased",0)
  res["magnitude_analyzed"]=comp_ok and par_ok and mag_ok
 res["labtainer_outputs_ready"]=all(res.get(n,False) for n in CHECKS[:-1])
 return res
def main():
 p=argparse.ArgumentParser(description="Validate VP9 directed parity coefficient stego lab work."); p.add_argument("--base",default=os.getcwd()); a=p.parse_args(); r=evaluate(a.base)
 for n in CHECKS: print(("Y" if r.get(n,False) else "N")+" - "+n)
 if not all(r.get(n,False) for n in CHECKS): sys.exit(1)
if __name__=="__main__": main()
