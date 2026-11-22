// Renderiza HTML a PNG para historias de Instagram (default 1080x1920).
// Uso: NODE_PATH=$(npm root -g) node plantilla/shot_story.js <html...>
// Tamaño opcional: SHOT_W=1080 SHOT_H=1920 (no toca shot.js, que sigue en 1080x1350).
const { chromium } = require('playwright');
(async () => {
  const W = parseInt(process.env.SHOT_W || '1080', 10);
  const H = parseInt(process.env.SHOT_H || '1920', 10);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: W, height: H } });
  for (const f of process.argv.slice(2)) {
    await p.goto('file://' + f); await p.waitForTimeout(400);
    await p.screenshot({ path: f.replace('.html', '.png') });
  }
  await b.close();
})();
