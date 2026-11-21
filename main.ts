// Leonida Lottery — a GTA 6 launch-week meme, posted on X.
//
// The post is the entry. This repository names it in POST.json; the
// house reads the post itself from X (its first picture and its text)
// and the judge scores what the house read — nothing written here
// about the post is judged. So this program has exactly one job: hand
// in the two files that belong to the entry, whole and unchanged.
//
//   POST.json — the address of Ora's post. Before it is copied, it is
//     held to the gate's own limits for the file: a JSON object of at
//     most 16,384 bytes, carrying a "url" string of at most 2,048
//     characters.
//
//   meme.png — the picture the post carries: the Leonida State
//     Lottery's "OFFICIAL WINNING TICKET" (draw date 19 NOV 2026),
//     drawn by build_memes.py. All six numbers matched — 13 years,
//     2 delays, 214 GB, the 19th, the 11th month, year 26 — days
//     waited 4,811, jackpot $3.79B of day-one sales, and the actual
//     prize one $79.99 copy of the game. make.fun's ghost is worked
//     into the ticket and its claim line reads "PAID BY MY AI AGENT
//     ON MAKE.FUN". This bounty sets no canvas or byte cap on the
//     shipped picture (the house shrinks the post's photo itself for
//     the dossier), so what is proved below is wholeness: the PNG
//     signature, the canvas size from IHDR, and a walk over every
//     chunk verifying its CRC-32, ending exactly at IEND.

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const botDir = process.env.MAKEFUN_BOT_DIR ?? dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });

// --- POST.json: read it, hold it to the gate's limits, hand it in ----

const postRaw = readFileSync(join(botDir, 'POST.json'));
if (postRaw.byteLength > 16_384) {
  throw new Error(`POST.json runs to ${postRaw.byteLength} bytes; the cap is 16,384`);
}

let parsed: unknown;
try {
  parsed = JSON.parse(postRaw.toString('utf8'));
} catch {
  throw new Error('POST.json does not parse as JSON');
}
if (parsed === null || typeof parsed !== 'object' || Array.isArray(parsed)) {
  throw new Error('POST.json is not a JSON object');
}

const url = (parsed as Record<string, unknown>).url;
if (typeof url !== 'string' || url.length === 0) {
  throw new Error('POST.json has no "url" string to hand in');
}
if (url.length > 2_048) {
  throw new Error(`the post url runs to ${url.length} characters; the cap is 2,048`);
}

// The address's shape (an X post: /<handle>/status/<digits>) is the
// gate's to refuse, not this program's to fix — but a string that is
// plainly not that shape means the wrong file was shipped, so say so.
if (!/^https:\/\/(www\.|mobile\.)?(x|twitter)\.com\/[^/]+\/status\/\d+$/.test(url)) {
  throw new Error(`"${url}" is not the address of a post on X`);
}

writeFileSync(join(outDir, 'POST.json'), postRaw);

// --- meme.png: prove the ticket whole, then hand it in --------------

const png = readFileSync(join(botDir, 'meme.png'));

// Every PNG opens with the same eight bytes. If they are not there,
// whatever this file is, it is not the ticket.
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (png.byteLength < PNG_SIGNATURE.byteLength || !png.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error('meme.png does not open with the PNG signature');
}

// IHDR is the first chunk; its data opens at byte 16 with the canvas
// width and height as big-endian uint32s.
const width = png.readUInt32BE(16);
const height = png.readUInt32BE(20);
if (width === 0 || height === 0) {
  throw new Error(`the ticket's canvas reads ${width}x${height} — no canvas at all`);
}

// A header can promise a whole picture over a truncated file, so walk
// the chunks. Each is: a uint32 data length, a four-letter type, the
// data, and a CRC-32 (PNG polynomial 0xEDB88320) over the type bytes
// and data bytes together. The stored CRC must equal the computed
// one, no chunk may run past the end of the file, and the walk must
// finish exactly on an empty IEND — nothing before it missing,
// nothing after it trailing.
const crcLut = new Uint32Array(256);
for (let n = 0; n < 256; n++) {
  let c = n;
  for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
  crcLut[n] = c >>> 0;
}
function crc32(buf: Buffer, from: number, to: number): number {
  let c = 0xffffffff;
  for (let i = from; i < to; i++) c = crcLut[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

const chunkTypes: string[] = [];
let offset = 8;
let sawPixelData = false;
let sawEndMarker = false;
while (offset < png.byteLength) {
  if (offset + 12 > png.byteLength) {
    throw new Error('the file ends inside a chunk header');
  }
  const dataLength = png.readUInt32BE(offset);
  const type = png.toString('latin1', offset + 4, offset + 8);
  const dataStart = offset + 8;
  const dataEnd = dataStart + dataLength;
  const crcEnd = dataEnd + 4;
  if (crcEnd > png.byteLength) {
    throw new Error(`chunk ${type} runs past the end of the file`);
  }
  if (crc32(png, offset + 4, dataEnd) !== png.readUInt32BE(dataEnd)) {
    throw new Error(`CRC-32 mismatch in chunk ${type}`);
  }
  if (chunkTypes.length === 0 && type !== 'IHDR') {
    throw new Error(`the first chunk is ${type}; a PNG opens with IHDR`);
  }
  if (type === 'IDAT') sawPixelData = true;
  if (type === 'IEND') {
    if (dataLength !== 0) throw new Error('the IEND chunk carries data');
    if (crcEnd !== png.byteLength) throw new Error('bytes trail the IEND chunk');
    sawEndMarker = true;
  }
  chunkTypes.push(type);
  offset = crcEnd;
}
if (!sawPixelData) throw new Error('no IDAT chunk — the ticket has no picture in it');
if (!sawEndMarker) throw new Error('no IEND chunk — the file is cut short');

writeFileSync(join(outDir, 'meme.png'), png);
console.log(`POST.json handed in: ${postRaw.byteLength} bytes, url of ${url.length} characters`);
console.log(
  `meme.png handed in: ${png.byteLength} bytes, ${width}x${height}, ` +
    `${chunkTypes.length} chunks CRC-verified (${chunkTypes.join(', ')})`,
);
