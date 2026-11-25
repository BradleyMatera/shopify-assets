/* Run after generation: node integration/check_gallery.cjs */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const crypto = require("node:crypto");
const base = __dirname;
class Node {
  constructor(tag) { this.tag=tag; this.children=[]; this.listeners={}; this.value=""; this.textContent=""; this.hidden=false; this.attrs={}; }
  append(...items){for(const n of items){if(n.tag==="fragment")this.children.push(...n.children);else this.children.push(n);}}
  replaceChildren(...items){this.children=[];this.append(...items);}
  querySelector(tag){for(const n of this.children){if(n.tag===tag)return n;const out=n.querySelector(tag);if(out)return out;}return null;}
  setAttribute(key,value){this.attrs[key]=value;}
  addEventListener(k,fn){this.listeners[k]=fn;}
  focus(){this.focused=true;}
}
const ids=Object.fromEntries("grid more search family format total families results filters package-logo wordmark-fallback".split(" ").map(x=>[x,new Node("el")]));
const document={getElementById:key=>ids[key],createElement:tag=>new Node(tag),createDocumentFragment:()=>new Node("fragment")};
const window={};
const ctx=vm.createContext({window,document,setTimeout:callback=>callback()});
vm.runInContext(fs.readFileSync(path.join(base,"gallery-manifest.js"),"utf8"),ctx);
const original=window.MDB_GALLERY.assets;
assert(original.length>0,"Generate a final manifest from a real asset tree before testing");
assert.equal(new Set(original.map(row=>row.path)).size,original.length);
for (const item of original){
  const file=path.resolve(base,item.path);
  assert(file.startsWith(path.dirname(base)+path.sep) && !file.startsWith(base+path.sep),item.path);
  const data=fs.readFileSync(file);
  assert.equal(data.length,item.bytes,item.path);
  assert.equal(crypto.createHash("sha256").update(data).digest("hex"),item.sha256,item.path);
}
const jsonFile=path.join(base,"gallery-manifest.json");
if(fs.existsSync(jsonFile))assert.equal(JSON.stringify(window.MDB_GALLERY),JSON.stringify(JSON.parse(fs.readFileSync(jsonFile,"utf8"))),"JS/JSON disagree");
const html=fs.readFileSync(path.join(base,"index.html"),"utf8");
for(const m of html.matchAll(/(?:href|src)="([^"#]+)"/g)){assert(!m[1].includes(":"));assert(fs.existsSync(path.resolve(base,m[1])),m[1]);}
window.MDB_GALLERY={schema:1,assets:[...original, {...original[0],title:"Invalid remote record",path:"//external.invalid/a.svg"}]};
vm.runInContext(fs.readFileSync(path.join(base,"gallery.js"),"utf8"),ctx);
assert.equal(ids.total.textContent,original.length.toLocaleString("en-US"));
assert.equal(ids.grid.children.length,Math.min(24,original.length));
if(original.length>24) {
  ids.more.listeners.click(); assert.equal(ids.grid.children.length,Math.min(48,original.length));
  assert(ids.grid.children[24].querySelector("a").focused,"New row has keyboard focus");
}
ids.search.value="not-an-asset-in-this-candidate"; ids.search.listeners.input();assert(ids.grid.children[0].textContent.includes("No matching"));
ids.search.value=""; ids.family.value=original[0].family; ids.family.listeners.change();
assert.equal(ids.grid.children.length,Math.min(24,original.filter(row=>row.family===ids.family.value).length));
ids.format.value=original[0].format;ids.format.listeners.change();
assert.equal(ids.grid.children.length,Math.min(24,original.filter(row=>row.family===ids.family.value&&row.format===ids.format.value).length));
assert(ids.grid.children[0].querySelector("a").download.includes("."),"Direct file download");
const gif=original.find(row=>row.format==="gif"&&!row.poster);
if(gif){ids.family.value="";ids.format.value="gif";ids.format.listeners.change();assert(!ids.grid.children[0].querySelector("img"),"No automatic inline GIF");}
ids.family.value="";ids.format.value="";ids.filters.listeners.reset();assert.equal(ids.grid.children.length,Math.min(24,original.length));
if(ids["package-logo"].listeners.load){ids["package-logo"].listeners.load();assert.equal(ids["wordmark-fallback"].hidden,true);}
console.log(`Gallery QA passed for ${original.length} actual files: manifest parity, safe local paths, every byte/hash, filter/search/reset, pagination/focus, downloads and fallback. DOM mock, not a browser render.`);
