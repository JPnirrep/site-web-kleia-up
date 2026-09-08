// Verif finale : lignes du H1 (point + majuscule) + aucun ':' orphelin en debut de ligne sur TOUTE la page.
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
const page = await browser.newPage();
await page.setViewport({ width: 1280, height: 700, deviceScaleFactor: 1.5 });

const targets = process.argv.slice(2);
const list = targets.length ? targets : ['retour-vacances-turbulences', 'ce-que-tu-vis-interieur'];

for (const t of list) {
  await page.goto(`file:///home/debian/workspace/site-web-kleia-up/journal/${t}.html`, {
    waitUntil: 'networkidle0', timeout: 30000
  });
  await new Promise(r => setTimeout(r, 1200));
  const res = await page.evaluate(() => {
    const h1 = document.querySelector('h1.hero-title');
    const range = document.createRange();
    const lineMap = [];
    let lastTop = null, current = [];
    const walker = document.createTreeWalker(h1, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    for (const tn of nodes) {
      const re = /\S+/g;
      let m;
      while ((m = re.exec(tn.textContent)) !== null) {
        range.setStart(tn, m.index);
        range.setEnd(tn, m.index + m[0].length);
        const rect = range.getBoundingClientRect();
        if (lastTop === null || Math.abs(rect.top - lastTop) > 5) {
          if (current.length) lineMap.push(current.join(' '));
          current = [m[0]];
          lastTop = rect.top;
        } else { current.push(m[0]); lastTop = rect.top; }
      }
    }
    if (current.length) lineMap.push(current.join(' '));
    // scan ':' en debut de ligne sur tous les titres et labels
    const colonIssues = [];
    for (const el of document.querySelectorAll('h1, h2, h3, .hero-subtitle, .post-date')) {
      const r = document.createRange();
      const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
      const tns = [];
      while (w.nextNode()) tns.push(w.currentNode);
      let top = null, line = [];
      for (const tn of tns) {
        const re2 = /\S+/g;
        let m2;
        while ((m2 = re2.exec(tn.textContent)) !== null) {
          r.setStart(tn, m2.index);
          r.setEnd(tn, m2.index + m2[0].length);
          const rect = r.getBoundingClientRect();
          if (top === null || Math.abs(rect.top - top) > 5) {
            if (line.length) {
              const L = line.join(' ');
              if (L.startsWith(':')) colonIssues.push(el.tagName + ': "' + L.slice(0, 50) + '"');
            }
            line = [m2[0]]; top = rect.top;
          } else { line.push(m2[0]); }
        }
      }
      if (line.length) {
        const L = line.join(' ');
        if (L.startsWith(':')) colonIssues.push(el.tagName + ': "' + L.slice(0, 50) + '"');
      }
    }
    return { lines: lineMap, colonIssues };
  });
  console.log('==', t);
  res.lines.forEach((l, i) => console.log(`  L${i + 1}: ${l}`));
  console.log('  deux-points orphelins:', res.colonIssues.length ? res.colonIssues : 'AUCUN');
}
await browser.close();
