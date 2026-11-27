#!/usr/bin/env python3
"""Read-only QA for organic campaign manifests (Python 3.8+, optional macOS curl).
JSON array or {"campaigns":[...]}; per row:
{"id":"unique", "platform":"facebook", "copy":"...", "url":"https://...",
 "state":"draft|scheduled|live|unpublished|failed",
 "scheduled_at":"2026-11-28T09:00:00-06:00",
 "published_at":"2026-11-28T09:00:03-06:00",
 "platform_post_id":"...", "live_url":"https://www.facebook.com/...",
 "expected_path":"/products/flour-sack-kitchen-towels",
 "expected_variant":"68068214472932"}
By default checks manifest evidence only. --network also checks public landing HTTP
for safe allowlisted Shopify GETs (no cart writes, checkout or social logins).
"""
import argparse, datetime as dt, json, re, subprocess, sys, unicodedata
from collections import Counter
from urllib.parse import parse_qs, urlsplit
HOST="materadigitalboutique.myshopify.com"
LANDING = re.compile(r"^/(?:$|(?:products|collections|pages|blogs|policies)(?:/[a-zA-Z0-9_-]+){1,3}/?$)")
SOURCE={"facebook":"facebook","instagram":"instagram","pinterest":"pinterest","youtube":"youtube","shop":"shop","x":"x","threads":"threads","tiktok":"tiktok"}
SOCIAL_HOST={"facebook":{"facebook.com","www.facebook.com","m.facebook.com","fb.watch"},"instagram":{"instagram.com","www.instagram.com"},"pinterest":{"pinterest.com","www.pinterest.com","pin.it"},"youtube":{"youtube.com","www.youtube.com","youtu.be"},"shop":{"shop.app","www.shop.app"},"x":{"x.com","www.x.com"},"threads":{"threads.net","www.threads.net","threads.com","www.threads.com"},"tiktok":{"tiktok.com","www.tiktok.com"}}
CLAIMS={
 "certification": r"\bcertified\b|\b(?:GOTS|OEKO[ -]?TEX|USDA organic|FSC)\b",
 "shipping_promise": r"\bfree shipping\b|\b(?:ships?|deliver(?:y|ed)) (?:today|tomorrow|next business day|within \d+|guaranteed)\b",
 "discount_or_scarcity": r"\b\d+\s*%\s*off\b|\blowest price\b|\b(?:only \d+ left|selling fast|best[ -]?sell(?:er|ing)|limited stock|sold out soon)\b",
 "absolute_or_environmental": r"\b(?:eco[ -]?friendly|sustainable|non[ -]?toxic|chemical[ -]?free|BPA[ -]?free|waterproof|guaranteed)\b|(?<![0-9])100\s*%",
 "returns_promise": r"\bfree returns\b|\bno[ -]?questions[ -]?asked\b|\brisk[ -]?free\b",
}
OLD = re.compile(r"real\s*mall\s*of\s*america|online mall",re.I)
def timestamp(z):
 if not z or not isinstance(z,str): return None
 try:
  t=dt.datetime.fromisoformat(z.replace("Z","+00:00")); return t if t.utcoffset() is not None else None
 except ValueError: return None
def normalize(s):
 s=re.sub(r"https?://\S+","",unicodedata.normalize("NFKC",s.lower()))
 return " ".join(re.findall(r"\w+",s))
def network(url, variant):
 # Never follow user-supplied redirects, even on a correct starting host.
 args=["curl","-sS","--max-time","9","--proto","=https","-w","\n%{http_code}",url]
 result=subprocess.run(args, capture_output=True,text=True)
 if result.returncode:return None,"network read failed: "+result.stderr.strip()
 body, code=result.stdout.rsplit("\n",1); code=int(code)
 if code==429:return None,"HTTP 429; landing not independently verified"
 if code!=200:return False,"HTTP "+str(code)
 if variant:
  if not re.search(r"<input\b(?=[^>]*\bname=[\"']id[\"'])(?=[^>]*\bvalue=[\"']"+re.escape(variant)+r"[\"'])[^>]*>",body,re.I):
   return False,"HTTP 200 but expected variant is not selected in cart form"
 return True,"HTTP 200" + (" and exact selected variant in form" if variant else "")
def audit(rows, check_network=False, now=None):
 now=now or dt.datetime.now(dt.timezone.utc); reports=[]; seen_copy={}; seen_ids=set(); attribution={}; calendar={}; observed={}
 for i,r in enumerate(rows,1):
  report={"id":r.get("id") or f"row-{i}","platform":r.get("platform"),"declared_state":r.get("state"),"evidence":[],"errors":[],"flags":[]}; reports.append(report)
  e=report["errors"]; f=report["flags"]; platform=str(r.get("platform") or "").lower(); state=str(r.get("state") or "").lower(); content=str(r.get("copy") or ""); key=normalize(content)
  if not r.get("id"):e.append("missing id")
  if report["id"] in seen_ids:e.append("duplicate campaign id")
  seen_ids.add(report["id"])
  if platform not in SOURCE:e.append("unknown platform")
  if not key:e.append("copy is empty")
  elif (platform,key) in seen_copy:f.append("duplicate platform copy: "+seen_copy[(platform,key)])
  elif any(k==key for _,k in seen_copy):f.append("same copy reused cross-platform; verify intentional")
  if key and (platform,key) not in seen_copy:seen_copy[(platform,key)]=report["id"]
  if OLD.search(content):e.append("legacy mall branding in copy")
  for category, pattern in CLAIMS.items():
   if re.search(pattern,content,re.I):f.append("claim requires verified evidence: "+category)
  raw=str(r.get("url") or "")
  try:u=urlsplit(raw);params=parse_qs(u.query,keep_blank_values=True);valid=u.scheme=="https" and u.netloc==HOST and u.fragment=="" and bool(LANDING.fullmatch(u.path or "/"))
  except ValueError: u=urlsplit("");params={};valid=False
  if not valid:e.append("landing must use HTTPS Boutique host and approved public route")
  path=u.path or "/"; expected=str(r.get("expected_path") or "")
  if not expected:f.append("expected_path missing; not checked against intended page")
  elif expected!=path:e.append("landing path differs from expected_path")
  variant=str(r.get("expected_variant") or "")
  if variant and (not variant.isdigit() or not path.startswith("/products/") or params.get("variant")!=[variant]):e.append("missing/wrong/duplicate exact product variant")
  elif not variant and path.startswith("/products/"):f.append("product link has no exact expected_variant")
  allowed={"utm_source","utm_medium","utm_campaign","utm_content","utm_term","variant"}
  unknown=set(params)-allowed
  if unknown:f.append("unexpected query keys: "+", ".join(sorted(unknown)))
  for field in ("utm_source","utm_medium","utm_campaign","utm_content"):
   v=params.get(field,[])
   if len(v)!=1 or not re.fullmatch(r"[a-z0-9][a-z0-9_-]*",v[0]):e.append("missing/duplicate/invalid "+field)
  if platform in SOURCE and params.get("utm_source")!=[SOURCE[platform]]:e.append("utm_source does not match channel")
  if params.get("utm_medium")!=["organic_social"]:e.append("utm_medium should be organic_social; don't count as paid")
  if all(len(params.get(k,[]))==1 for k in ("utm_source","utm_medium","utm_campaign","utm_content")):
   a=tuple(params[k][0] for k in ("utm_source","utm_medium","utm_campaign","utm_content"))
   if a in attribution:f.append("UTM attribution collision: "+attribution[a])
   attribution.setdefault(a,report["id"])
  planned=timestamp(r.get("scheduled_at")); posted=timestamp(r.get("published_at")); post_id=r.get("platform_post_id"); live=str(r.get("live_url") or "")
  if state not in {"draft","scheduled","live","unpublished","failed"}:e.append("state must be draft, scheduled, live, unpublished or failed")
  if r.get("scheduled_at") and not planned:e.append("scheduled_at must be ISO 8601 with explicit timezone")
  if r.get("published_at") and not posted:e.append("published_at must be ISO 8601 with explicit timezone")
  if state=="scheduled":
   if not planned:e.append("scheduled state requires a valid scheduled_at")
   if not post_id:f.append("no native schedule reference; treat as planned, not confirmed scheduled")
   if planned and planned<=now:f.append("scheduled time passed; verify native publication")
   if posted or live:e.append("scheduled row contains published evidence; reconcile native status")
  if state=="live":
   if not posted or posted>now:e.append("live requires a past published_at")
   try:w=urlsplit(live); good=w.scheme=="https" and w.netloc in SOCIAL_HOST.get(platform,set()) and w.path not in {"","/"}
   except ValueError:good=False
   if not post_id or not good:e.append("live requires native post ID and platform permalink")
   if not report["errors"]: report["evidence"].append("live evidence recorded in manifest; not independently verified on platform")
  if state in {"draft","failed"} and (posted or live):f.append("non-live state contains publication evidence; reconcile native status")
  if planned and state in {"scheduled","live"}:
   c=(platform,planned.astimezone(dt.timezone.utc))
   if c in calendar:f.append("same platform and scheduled time: "+calendar[c])
   calendar.setdefault(c,report["id"])
  if check_network and valid:
   clean=f"https://{HOST}{path}"+(f"?variant={variant}" if variant.isdigit() else "")
   if clean not in observed:observed[clean]=network(clean,variant if variant.isdigit() else "")
   ok, detail=observed[clean]
   (report["evidence"] if ok else f if ok is None else e).append(detail)
 return reports
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("manifest");p.add_argument("--network",action="store_true");p.add_argument("--strict",action="store_true",help="fail on flags as well as errors");a=p.parse_args()
 try:
  with open(a.manifest,encoding="utf-8") as h:d=json.load(h)
  rows=d.get("campaigns") if isinstance(d,dict) else d
  if not isinstance(rows,list) or not rows or not all(isinstance(r,dict) for r in rows):raise ValueError("manifest needs a nonempty campaign list")
 except (ValueError,OSError) as x:print(x,file=sys.stderr);return 2
 reports=audit(rows,a.network);n=sum(bool(r["errors"]) for r in reports);k=sum(bool(r["flags"]) for r in reports)
 print(json.dumps({"rows":len(reports),"rows_with_errors":n,"rows_with_flags":k,"results":reports},indent=2))
 return 1 if n or (a.strict and k) else 0
if __name__=="__main__":sys.exit(main())
