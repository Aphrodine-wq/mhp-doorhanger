#!/usr/bin/env node
// Standalone QR generator for the MHP door-hanger campaign.
// Run from this folder:    node generate-qr.js
// Or, with npx (no install needed if you bump the QR_URL):
//                          npx qrcode "$URL" -o doorhanger.png -t png --error-correction-level H
//
// Edit QR_URL below to point at whichever host you drop index.html on
// (Netlify Drop, S3, Vercel, GitHub Pages, etc.). Brand colors stay consistent.

const { writeFile } = require('node:fs/promises');
const { join } = require('node:path');

// Deployed via GitHub Pages from Aphrodine-wq/mhp-doorhanger.
// To migrate hosts later: change this URL, run `node generate-qr.js`, then run composite-hanger.py.
const QR_URL =
  'https://aphrodine-wq.github.io/mhp-doorhanger/?src=doorhanger&utm_source=doorhanger&utm_medium=print&utm_campaign=oxford_2026q2';

const BRAND_DARK = '#0b3d91';
const BRAND_LIGHT = '#fbfaf6';

async function main() {
  let QRCode;
  try {
    QRCode = require('qrcode');
  } catch {
    console.error('Missing dep. Install it first:\n  npm i -g qrcode\nor run inline:\n  npx qrcode "' + QR_URL + '" -o doorhanger.png -t png --error-correction-level H');
    process.exit(1);
  }

  const opts = {
    errorCorrectionLevel: 'H',
    margin: 2,
    color: { dark: BRAND_DARK, light: BRAND_LIGHT },
  };

  const svg = await QRCode.toString(QR_URL, { type: 'svg', ...opts });
  await writeFile(join(__dirname, 'doorhanger.svg'), svg, 'utf8');

  const png = await QRCode.toBuffer(QR_URL, { type: 'png', width: 1024, ...opts });
  await writeFile(join(__dirname, 'doorhanger.png'), png);

  console.log('Encoded URL:', QR_URL);
  console.log('Wrote:');
  console.log('  ' + join(__dirname, 'doorhanger.svg'));
  console.log('  ' + join(__dirname, 'doorhanger.png'));
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
