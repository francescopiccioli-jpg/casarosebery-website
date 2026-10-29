// Uso: python3 stampa-src/genera_menu_pdf.py <cartella> --definitivo && node stampa-src/pdf.js <cartella> --definitivo
const {chromium}=require('playwright');const BOZZA=!process.argv.includes('--definitivo');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});const p=await b.newPage();
for (const [f,o,l] of (process.argv.includes('--en')?[['menu_en.html','menu_en.pdf',false]]:[['menu.html','menu.pdf',false],['verifica.html','verifica.pdf',true]])){
await p.goto('file://'+process.argv[2]+'/'+f);await p.waitForTimeout(400);
await p.pdf({path:process.argv[2]+'/'+o,format:'A4',landscape:l,printBackground:true,preferCSSPageSize:true,displayHeaderFooter:!l,headerTemplate:'<span></span>',footerTemplate:'<div style="width:100%;text-align:center;font-size:7pt;color:#9a9080;font-family:Inter">Casa Rosebery · <span class=pageNumber></span>'+(BOZZA?' · <span style="color:#a3412b;letter-spacing:1px">BOZZA · allergeni da confermare in cucina prima della stampa</span>':'')+'</div>'});}
await b.close();})();
