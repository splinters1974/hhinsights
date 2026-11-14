#!/usr/bin/env node
// Browser smoke tests for the branch's static site, not the live website.
import { spawn } from 'node:child_process';
import { setTimeout as delay } from 'node:timers/promises';
import fs from 'node:fs';
import { chromium } from 'playwright';

const base='http://127.0.0.1:8765/';
const server=spawn('python3',['-m','http.server','8765','--directory','site'],{stdio:'ignore'});
const errors=[];
const output='phase1-browser-screenshots';
fs.mkdirSync(output,{recursive:true});
async function loadServer(){
 for(let i=0;i<50;i++){
  try{const r=await fetch(base+'index.html');if(r.ok)return;}catch{}
  await delay(200);
 }
 throw new Error('Local static server did not start');
}
function assert(condition,message){if(!condition)errors.push(message);}
async function checkImageLoad(page,label){
 // Lazy images do not start loading until they are near the viewport.
 // Scroll each image into view first and wait for its load/decode outcome.
 const images=page.locator('img[src]');
 for(let i=0;i<await images.count();i++){
   const img=images.nth(i);
   await img.scrollIntoViewIfNeeded();
   try{
     await img.evaluate(async node=>{
       if(!node.complete)await new Promise((resolve,reject)=>{
         node.addEventListener('load',resolve,{once:true});
         node.addEventListener('error',reject,{once:true});
       });
       if(node.decode && node.naturalWidth>0)await node.decode();
     },{timeout:10000});
   }catch(e){errors.push(label+': image load error: '+await img.getAttribute('src')+' ('+String(e).slice(0,120)+')');}
 }
 const bad=await images.evaluateAll(nodes=>nodes.filter(n=>n.complete&&n.naturalWidth===0).map(n=>n.getAttribute('src')));
 assert(bad.length===0,label+': failed images: '+bad.join(', '));
}
try{
 await loadServer();
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 for(const view of [{label:'desktop',width:1365,height:900},{label:'mobile',width:390,height:844}]){
  const context=await browser.newContext({viewport:{width:view.width,height:view.height},deviceScaleFactor:1});
  const page=await context.newPage();
  for(const route of ['index.html','guides.html','sectors.html','sample-report.html','contact.html','analyser/']){
   const resp=await page.goto(base+route,{waitUntil:'domcontentloaded',timeout:60000});
   assert(resp?.status()===200,view.label+' '+route+': response '+resp?.status());
   if(route==='index.html'){
    assert(await page.locator('h1').count()>0,view.label+': home heading absent');
    assert(await page.locator('a[href="sample-report.html"]').count()>0,view.label+': missing sample link');
   }
   if(route==='sample-report.html')assert((await page.locator('body').innerText()).includes('Demonstration only'),view.label+': sample disclaimer missing');
   if(route==='contact.html'){
    assert(await page.locator('form[name="enquiry"]').count()===1,view.label+': enquiry form missing');
    assert(await page.locator('a[href^="mailto:"]').count()>0,view.label+': email fallback missing');
   }
   if(route==='analyser/')await page.waitForTimeout(1800);
   if(route!=='analyser/')await checkImageLoad(page,view.label+' '+route);
   if(['index.html','guides.html','sample-report.html','analyser/'].includes(route)){
    await page.screenshot({path:output+'/'+view.label+'-'+route.replaceAll('/','').replace('.html','')+'.png',fullPage:false});
   }
  }
  await context.close();
 }
 await browser.close();
}finally{server.kill('SIGTERM');}
console.log(JSON.stringify({checks:'static browser smoke tests',errors,screenshots:output},null,2));
if(errors.length)process.exit(1);
