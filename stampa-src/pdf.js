// Uso: python3 stampa-src/genera_menu_pdf.py <cartella> --definitivo && node stampa-src/pdf.js <cartella> --definitivo
//      python3 stampa-src/genera_vini_pdf.py <cartella> [--web] && node stampa-src/pdf.js <cartella> --vini
const {chromium}=require('playwright');const BOZZA=!process.argv.includes('--definitivo');const VINI=process.argv.includes('--vini');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
const lista = VINI ? [['vini.html','vini.pdf',false]] : (process.argv.includes('--en')?[['menu_en.html','menu_en.pdf',false]]:[['menu.html','menu.pdf',false],['verifica.html','verifica.pdf',true]]);
for (const [f,o,l] of lista){
await p.goto('file://'+process.argv[2]+'/'+f);await p.waitForTimeout(400);
const piede = VINI
  ? '<div style="width:100%;text-align:center;font-size:7pt;color:#9a9080;font-family:Inter">Casa Rosebery · Carta dei vini · <span class=pageNumber></span></div>'
  : '<div style="width:100%;text-align:center;font-size:7pt;color:#9a9080;font-family:Inter">Casa Rosebery · <span class=pageNumber></span>'+(BOZZA?' · <span style="color:#a3412b;letter-spacing:1px">BOZZA · allergeni da confermare in cucina prima della stampa</span>':'')+'</div>';
await p.pdf({path:process.argv[2]+'/'+o,...(l?{format:'A4',landscape:true}:{}),printBackground:true,preferCSSPageSize:true,displayHeaderFooter:VINI,headerTemplate:'<span></span>',footerTemplate:piede});}
await b.close();})();
