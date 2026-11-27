(() => {
  "use strict";
  const manifest = window.MDB_GALLERY;
  const el = id => document.getElementById(id);
  const list = el("grid"), more = el("more"), search = el("search"), family = el("family"), format = el("format");
  const create = (tag, cls, value) => {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (value !== undefined) node.textContent = value;
    return node;
  };
  const types = new Set(["png", "jpg", "jpeg", "webp", "avif", "svg", "ico", "gif", "mp4", "webm", "pdf", "zip", "json", "css", "liquid"]);
  const local = value => typeof value === "string" && /^(?:\.\.\/)?[A-Za-z0-9_./%-]+$/.test(value) && !value.startsWith("/") && !value.slice(value.startsWith("../") ? 3 : 0).split("/").includes("..") && !/%(?:2e|2f|5c)/i.test(value);
  const hasShape = row => row && local(row.path) && typeof row.title === "string" && typeof row.family === "string" && types.has(row.format);
  const rows = Array.isArray(manifest?.assets) ? manifest.assets.filter(hasShape) : [];
  const families = [...new Set(rows.map(row => row.family))];
  const formats = [...new Set(rows.map(row => row.format))].sort();
  const collate = (a,b) => a.localeCompare(b,"en",{numeric:true});
  const fillOptions = (select, values, label) => {
    for (const v of values) {
      const option = create("option", "", label(v));
      option.value = v;
      select.append(option);
    }
  };
  fillOptions(family, families.sort(collate), v => v);
  fillOptions(format, formats, v => v.toUpperCase());
  el("total").textContent = rows.length.toLocaleString("en-US");
  el("families").textContent = families.length.toLocaleString("en-US");
  let limit = 24;
  const imageKinds = new Set(["png","jpg","jpeg","webp","avif","svg","ico","gif"]);
  const motionKinds = new Set(["mp4","webm"]);
  const toRelative = value => value.split("/").map(s => s === ".." ? s : encodeURIComponent(s)).join("/");
  const logo = rows.find(row => row.path.endsWith("/identity/masters/mdb-horizontal-dark.svg"));
  if(logo) {
    const image=el("package-logo");
    image.addEventListener("load",()=>{image.hidden=false;el("wordmark-fallback").hidden=true;},{once:true});
    image.src=toRelative(logo.path);
  }
  const fmtSize = bytes => Number.isFinite(bytes) ? bytes > 1048576 ? (bytes/1048576).toFixed(1)+" MiB" : Math.ceil(bytes/1024)+" KiB" : "";
  const fallback = (container, kind) => container.replaceChildren(create("span", "type-fallback", kind.toUpperCase()));
  const card = row => {
    const item = create("article", "asset");
    const thumb = create("div", "thumb"+(row.tone === "light" ? " dark" : ""));
    if (row.format === "gif") {
      // Browsers can autoplay an img GIF even with reduced motion. Use a static poster or a file-type tile.
      if (local(row.poster)) {
        const img = create("img"); img.src=toRelative(row.poster); img.alt=""; img.loading="lazy"; thumb.append(img);
      } else fallback(thumb,row.format);
    } else if (imageKinds.has(row.format)) {
      const img = create("img"); img.src=toRelative(row.path); img.alt=""; img.loading="lazy"; img.decoding="async";
      img.addEventListener("error",()=>fallback(thumb,row.format),{once:true}); thumb.append(img);
    } else if (motionKinds.has(row.format)) {
      const v = create("video"); v.controls=true; v.playsInline=true; v.preload="none";
      v.setAttribute("aria-label",row.title+" motion preview");
      if (local(row.poster)) v.poster=toRelative(row.poster);
      v.src=toRelative(row.path); v.addEventListener("error",()=>fallback(thumb,row.format),{once:true}); thumb.append(v);
    } else fallback(thumb,row.format);
    const body = create("div","asset-body");
    const labels = create("div","type");
    labels.append(create("span","",row.family),create("span","asset-status",typeof row.status==="string" ? row.status : "Candidate"));
    const dims = Number.isFinite(row.width) && Number.isFinite(row.height) ? row.width+" × "+row.height : "";
    const meta = [row.format.toUpperCase(),dims,fmtSize(row.bytes)].filter(Boolean).join(" · ");
    const link = create("a","", "Download "+row.format.toUpperCase()); link.href=toRelative(row.path); link.download=row.path.split("/").pop();
    link.setAttribute("aria-label","Download "+row.title+" "+row.format.toUpperCase());
    body.append(labels,create("h3","",row.title),create("p","asset-meta",meta),link);
    item.append(thumb,body);
    return item;
  };
  function draw(){
    const keyword = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    const matches = rows.filter(row => (!family.value || row.family===family.value) && (!format.value || row.format===format.value) && keyword.every(k=>[row.title,row.path,row.family,row.format,row.status].join(" ").toLowerCase().includes(k)));
    const display = matches.slice(0,limit);
    el("results").textContent=rows.length ? "Showing "+display.length+" of "+matches.length+" matching asset"+(matches.length===1?"":"s") : "No media manifest has been generated for this delivery yet.";
    more.hidden = display.length===matches.length;
    const batch=document.createDocumentFragment();
    for (const row of display) batch.append(card(row));
    if (!display.length) batch.append(create("p","notice",rows.length ? "No matching assets. Try a different search or reset the filters." : "Use the included manifest generator after adding the approved candidate files. This gallery will not substitute sample files or pretend a release exists."));
    list.replaceChildren(batch);
  }
  const refilter=()=>{limit=24;draw();}; search.addEventListener("input",refilter); family.addEventListener("change",refilter); format.addEventListener("change",refilter);
  el("filters").addEventListener("submit",e=>e.preventDefault());
  el("filters").addEventListener("reset",()=>setTimeout(refilter,0));
  more.addEventListener("click",()=>{limit+=24;draw(); const focus=list.children[Math.max(0,limit-24)]?.querySelector("a"); if(focus) focus.focus();});
  draw();
})();
