#!/usr/bin/env node
// Make an excalidraw.com share link for an /architecture diagram.
//
//   node share.mjs FILE.excalidraw            upload, print https://excalidraw.com/#json=<id>,<key>
//   node share.mjs FILE.excalidraw --dry-run  encode and decode locally, upload nothing
//
// This does what Excalidraw's own "Share link" button does: the scene is compressed and
// encrypted here with a fresh AES-GCM key, only the ciphertext is uploaded to Excalidraw's
// JSON backend, and the key stays in the part of the link after #, which browsers never
// send to a server. Whoever has the link can read the diagram, so treat it like the diagram.
//
// Embedded images (the brand icons) are left out: the backend stores images separately,
// and the shared copy reads fine without them. Built-in Node modules only (Node 18+).
// Format mirrors packages/excalidraw/data/encode.ts (compressData) and encryption.ts.

import { readFileSync } from "node:fs";
import { deflateSync, inflateSync } from "node:zlib";
import { webcrypto as crypto } from "node:crypto";

const POST_URL = "https://json.excalidraw.com/api/v2/post/";
const IV_BYTES = 12;

function concatBuffers(...buffers) {
  const total = 4 + 4 * buffers.length + buffers.reduce((n, b) => n + b.byteLength, 0);
  const out = new Uint8Array(total);
  const view = new DataView(out.buffer);
  let cursor = 0;
  view.setUint32(cursor, 1); // CONCAT_BUFFERS_VERSION
  cursor += 4;
  for (const b of buffers) {
    view.setUint32(cursor, b.byteLength);
    cursor += 4;
    out.set(b, cursor);
    cursor += b.byteLength;
  }
  return out;
}

function splitBuffers(buf) {
  const view = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  const parts = [];
  let cursor = 4;
  while (cursor < buf.byteLength) {
    const size = view.getUint32(cursor);
    cursor += 4;
    parts.push(buf.slice(cursor, cursor + size));
    cursor += size;
  }
  return parts;
}

async function importKey(k, usage) {
  return crypto.subtle.importKey(
    "jwk",
    { alg: "A128GCM", ext: true, k, key_ops: ["encrypt", "decrypt"], kty: "oct" },
    { name: "AES-GCM", length: 128 },
    false,
    [usage],
  );
}

async function encode(sceneJson) {
  const key = await crypto.subtle.generateKey({ name: "AES-GCM", length: 128 }, true, ["encrypt", "decrypt"]);
  const k = (await crypto.subtle.exportKey("jwk", key)).k;
  const enc = new TextEncoder();
  const fileInfo = enc.encode(JSON.stringify({ version: 2, compression: "pako@1", encryption: "AES-GCM" }));
  const inner = concatBuffers(enc.encode(JSON.stringify(null)), enc.encode(sceneJson));
  const iv = crypto.getRandomValues(new Uint8Array(IV_BYTES));
  const encrypted = new Uint8Array(
    await crypto.subtle.encrypt({ name: "AES-GCM", iv }, await importKey(k, "encrypt"), deflateSync(inner)),
  );
  return { payload: concatBuffers(fileInfo, iv, encrypted), k };
}

async function decode(payload, k) {
  const [, iv, encrypted] = splitBuffers(payload);
  const plain = new Uint8Array(await crypto.subtle.decrypt({ name: "AES-GCM", iv }, await importKey(k, "decrypt"), encrypted));
  const [, data] = splitBuffers(new Uint8Array(inflateSync(plain)));
  return new TextDecoder().decode(data);
}

async function main() {
  const [file, flag] = process.argv.slice(2);
  if (!file) {
    console.error("usage: node share.mjs FILE.excalidraw [--dry-run]");
    process.exit(2);
  }
  const doc = JSON.parse(readFileSync(file, "utf8"));
  const elements = doc.elements.filter((e) => e.type !== "image");
  const sceneJson = JSON.stringify({
    type: "excalidraw",
    version: 2,
    source: "https://excalidraw.com",
    elements,
    appState: { viewBackgroundColor: doc.appState?.viewBackgroundColor ?? "#ffffff", gridSize: null },
  });
  const { payload, k } = await encode(sceneJson);

  if (flag === "--dry-run") {
    const back = JSON.parse(await decode(payload, k));
    const ok = back.elements.length === elements.length;
    console.log(`dry run: ${payload.byteLength} bytes encrypted, ${back.elements.length} elements decoded — ${ok ? "ok" : "MISMATCH"}`);
    process.exit(ok ? 0 : 1);
  }

  const res = await fetch(POST_URL, { method: "POST", body: payload });
  const json = await res.json().catch(() => ({}));
  if (!json.id) {
    const reason = json.error_class === "RequestTooLargeError" ? "the diagram is too large for a share link" : `HTTP ${res.status}`;
    console.error(`share failed: ${reason}. Open the file locally instead.`);
    process.exit(1);
  }
  console.log(`https://excalidraw.com/#json=${json.id},${k}`);
}

main().catch((err) => {
  console.error(`share failed: ${err.message}`);
  process.exit(1);
});
