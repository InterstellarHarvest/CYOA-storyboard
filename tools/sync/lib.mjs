// Shared, dependency-free helpers for the canonical storyboard sync tools (docs/105).
//
// Record keys name every image record in story/artwork.draft.json, including nested variants:
//   scenes:<id>                     main 314x206 scene
//   scenes:<id>#portraitBackground  opaque 564x278 closer view behind an NPC foreground
//   scenes:<id>#states:<stateId>    conditional scene state (layer replace = opaque, overlay = transparent)
//   portraits:<id>                  transparent 564x278 NPC foreground (or the parent of complete views)
//   portraits:<id>#views:<scene>    opaque-complete 564x278 conversation view (the House)
//   portraits:<id>#layers:<role>    a listed layer of a reused layered portrait
//   items:<id>#slot / #inspect      96x96 inventory slot / 565x451 inspection art
//   focus:<id>                      564x278 Focus A close-up
//   focus:<id>#pages:<n>            one page of a paged Focus A close-up
//   deathScreens:<id>               death / ending vignette
import fs from 'node:fs';
import zlib from 'node:zlib';
import crypto from 'node:crypto';

export const SELECTED = ['approved', 'integrated', 'reused'];
export const STATUS_VALUES = ['not-started', 'prompted', 'generated', 'approved', 'integrated', 'reused'];
// Presentation formats a record may declare. 'opaque-complete' (docs/92) is an image container;
// the two NO-IMAGE formats (docs/137, Nate 2026-11-24) are owner-approved presentation decisions
// that must never carry an image: 'text-led' scenes keep the previous scene image on screen (C1),
// 'voice-only' speakers lead dialogue in Narrative B without a portrait (C2).
export const FORMATS = { 'opaque-complete': 'portraits', 'text-led': 'scenes', 'voice-only': 'portraits' };
export const NO_IMAGE_FORMATS = ['text-led', 'voice-only'];

export const sha256 = (buf) => crypto.createHash('sha256').update(buf).digest('hex');
export const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));
export const writeJson = (file, value) => fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n');

// Every image record, in catalog order. `record` is the live object (mutations write through);
// `path` is the record's production assetPath (layers use `path`).
export function artRecords(art) {
  const out = [];
  const add = (key, record, extra) => out.push({ key, record, path: record.assetPath || record.path || null, ...extra });
  for (const [id, r] of Object.entries(art.scenes || {})) {
    add('scenes:' + id, r, { group: 'scenes', id });
    if (r.portraitBackground) add('scenes:' + id + '#portraitBackground', r.portraitBackground, { group: 'scenes', id, variant: 'portraitBackground', parent: r });
    (r.states || []).forEach((s) => add('scenes:' + id + '#states:' + s.id, s, { group: 'scenes', id, variant: 'states:' + s.id, parent: r }));
  }
  for (const [id, r] of Object.entries(art.portraits || {})) {
    add('portraits:' + id, r, { group: 'portraits', id });
    for (const [scene, v] of Object.entries(r.views || {})) add('portraits:' + id + '#views:' + scene, v, { group: 'portraits', id, variant: 'views:' + scene, parent: r });
    (r.layers || []).forEach((l) => add('portraits:' + id + '#layers:' + l.role, l, { group: 'portraits', id, variant: 'layers:' + l.role, parent: r, layer: true }));
  }
  for (const [id, r] of Object.entries(art.items || {})) {
    for (const v of Object.keys(r)) if (r[v] && typeof r[v] === 'object') add('items:' + id + '#' + v, r[v], { group: 'items', id, variant: v });
  }
  for (const [id, r] of Object.entries(art.focus || {})) {
    add('focus:' + id, r, { group: 'focus', id });
    (r.pages || []).forEach((p, i) => add('focus:' + id + '#pages:' + (i + 1), p, { group: 'focus', id, variant: 'pages:' + (i + 1), parent: r }));
  }
  for (const [id, r] of Object.entries(art.deathScreens || {})) add('deathScreens:' + id, r, { group: 'deathScreens', id });
  return out;
}

// A layer has no status of its own: it inherits its portrait's.
export const statusOf = (entry) => (entry.layer ? entry.parent.status : entry.record.status) || 'not-started';

// Expected kind/size/alpha for an image record. alpha: 'transparent' = must contain transparent
// pixels; 'opaque' = every pixel alpha 255. null = not constrained.
export function contractFor(entry) {
  const r = entry.record;
  const dims = (r.dimensions || (entry.layer ? entry.parent.dimensions : '') || '').match(/^(\d+)x(\d+)$/);
  const size = dims ? [Number(dims[1]), Number(dims[2])] : null;
  let alpha = null;
  const kind = r.kind || (entry.layer ? 'portrait-layer' : '');
  if (kind === 'scene' || kind === 'portrait-background' || kind === 'portrait-view' || kind === 'focus' || kind === 'focus-page' || kind === 'item-inspect' || kind === 'death-screen') alpha = 'opaque';
  if (kind === 'scene-state') alpha = r.layer === 'overlay' ? 'transparent' : 'opaque';
  if (kind === 'portrait') alpha = 'transparent';
  if (kind === 'item-slot') alpha = 'transparent';
  if (entry.layer) alpha = r.role === 'background' ? 'opaque' : 'transparent';
  return { kind, size, alpha };
}

// Minimal PNG decoder (8-bit gray/RGB/RGBA/palette, non-interlaced): enough to prove size and the
// transparency contract without a dependency.
export function decodePng(buf) {
  if (buf.length < 33 || buf.readUInt32BE(0) !== 0x89504e47) throw Error('not a PNG');
  let off = 8, width = 0, height = 0, depth = 0, ctype = 0, interlace = 0, plte = null, trns = null;
  const idat = [];
  while (off < buf.length) {
    const len = buf.readUInt32BE(off), type = buf.toString('ascii', off + 4, off + 8), data = buf.subarray(off + 8, off + 8 + len);
    if (type === 'IHDR') { width = data.readUInt32BE(0); height = data.readUInt32BE(4); depth = data[8]; ctype = data[9]; interlace = data[12]; }
    else if (type === 'PLTE') plte = data;
    else if (type === 'tRNS') trns = data;
    else if (type === 'IDAT') idat.push(data);
    else if (type === 'IEND') break;
    off += 12 + len;
  }
  const info = { width, height, depth, colorType: ctype };
  if (depth !== 8 || interlace) return { ...info, decoded: false };
  const channels = { 0: 1, 2: 3, 3: 1, 4: 2, 6: 4 }[ctype];
  const raw = zlib.inflateSync(Buffer.concat(idat));
  const stride = width * channels, px = Buffer.alloc(stride * height);
  let prev = Buffer.alloc(stride);
  for (let y = 0; y < height; y++) {
    const f = raw[y * (stride + 1)], line = raw.subarray(y * (stride + 1) + 1, (y + 1) * (stride + 1)), cur = px.subarray(y * stride, (y + 1) * stride);
    for (let x = 0; x < stride; x++) {
      const a = x >= channels ? cur[x - channels] : 0, b = prev[x], c = x >= channels ? prev[x - channels] : 0;
      let v = line[x];
      if (f === 1) v += a; else if (f === 2) v += b; else if (f === 3) v += (a + b) >> 1;
      else if (f === 4) { const p = a + b - c, pa = Math.abs(p - a), pb = Math.abs(p - b), pc = Math.abs(p - c); v += pa <= pb && pa <= pc ? a : pb <= pc ? b : c; }
      cur[x] = v & 255;
    }
    prev = cur;
  }
  let transparent = 0, partial = 0;
  for (let i = 0; i < width * height; i++) {
    let al = 255;
    if (ctype === 6) al = px[i * 4 + 3];
    else if (ctype === 4) al = px[i * 2 + 1];
    else if (ctype === 3 && trns) { const idx = px[i]; al = idx < trns.length ? trns[idx] : 255; }
    if (al === 0) transparent++; else if (al < 255) partial++;
  }
  return { ...info, decoded: true, transparent, partial, pixels: width * height };
}

export function checkContract(entry, buf) {
  const c = contractFor(entry), problems = [];
  let png;
  try { png = decodePng(buf); } catch (e) { return { problems: ['not a readable PNG: ' + e.message] }; }
  if (c.size && (png.width !== c.size[0] || png.height !== c.size[1])) problems.push('is ' + png.width + 'x' + png.height + ', record says ' + c.size.join('x'));
  if (png.decoded && c.alpha === 'opaque' && (png.transparent || png.partial)) problems.push('must be opaque but has ' + (png.transparent + png.partial) + ' non-opaque pixels');
  if (png.decoded && c.alpha === 'transparent' && !png.transparent) problems.push('must be a transparent RGBA foreground/overlay but has no transparent pixels');
  return { problems, png, contract: c };
}
