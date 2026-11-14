#!/usr/bin/env node
// Materialise the approved Phase 1 raster imagery from review-safe SVG assets.
// Only writes to the local working tree; the GitHub Actions workflow controls commits.
import fs from 'node:fs';
import path from 'node:path';

const root=path.resolve('site/images');
const names=[
 'guides','get-your-data','example-office-analysis','example-school-analysis',
 'reading-a-heatmap','out-of-hours-electricity','base-load','supply-capacity',
 'proving-savings','half-hourly-settlement','glossary','how-it-works',
 'schools-electricity','offices-council-buildings','leisure-centres',
 'healthcare-electricity','industrial-warehouses','retail-hospitality','sectors',
 'estate-town','town-street','faq','contact','contact-photo','og-image'
];
const photos=new Set(['estate-town','town-street','contact-photo']);
let count=0,bytes=0;
for(const name of names){
  const src=path.join(root,'phase1',name+'.svg');
  const svg=fs.readFileSync(src,'utf8');
  const match=svg.match(/href="data:image\/(jpeg|png);base64,([^"]+)"/);
  if(!match)throw new Error('Missing embedded raster data in '+name);
  const [,type,encoded]=match;
  const data=Buffer.from(encoded,'base64');
  const ext=type==='png'?'png':'jpg';
  const valid=type==='png'?data.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])):(data[0]===0xff&&data[1]===0xd8);
  if(!valid||data.length<1000)throw new Error('Corrupt asset '+name);
  const rel=name==='og-image'?'og-image.png':photos.has(name)?'photos/'+name+'.jpg':'guides/'+name+'.jpg';
  const target=path.join(root,rel);
  fs.mkdirSync(path.dirname(target),{recursive:true});
  fs.writeFileSync(target,data);
  count++;bytes+=data.length;
  console.log(rel+' '+data.length+' bytes');
}
if(count!==25)throw new Error('Expected 25 images, wrote '+count);
console.log('Materialised '+count+' image files ('+(bytes/1048576).toFixed(2)+' MiB)');
