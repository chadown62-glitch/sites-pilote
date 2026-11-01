// Contrôles reproductibles du pilote ; aucun téléchargement/achat automatique.
// Nécessite un Playwright et un Chromium DÉJÀ disponibles dans les quotas existants.
const fs = require("node:fs");
const path = require("node:path");
const http = require("node:http");
const assert = require("node:assert/strict");
const root = path.resolve(__dirname, "..");
const pages = ["index.html", "entreprise.html", "prestations.html", "peinture.html",
  "renovation-interieure.html", "realisations.html", "contact.html",
  "mentions-legales.html", "confidentialite.html"];
const allowed = new Set([...pages, "css/style.css", "js/main.js"]);
async function run() {
  let chromium;
  try {
    const modulePath = process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
    ({chromium} = require(modulePath ? path.join(modulePath, "playwright") : "playwright"));
    if (!fs.existsSync(chromium.executablePath())) throw Error("Chromium absent");
  } catch {
    console.error("NON VÉRIFIÉ : Playwright/Chromium déjà installé requis. Aucun téléchargement déclenché.");
    process.exitCode = 2;
    return;
  }
  const server = http.createServer((req, res) => {
    const name = (req.url || "/").split("?")[0].slice(1) || "index.html";
    if (!allowed.has(name)) { res.writeHead(404).end(); return; }
    const file = path.join(root, name);
    if (fs.lstatSync(file).isSymbolicLink()) { res.writeHead(403).end(); return; }
    res.setHeader("Content-Type", name.endsWith(".css") ? "text/css" :
      name.endsWith(".js") ? "text/javascript" : "text/html; charset=utf-8");
    res.setHeader("Cache-Control", "no-store");
    res.end(fs.readFileSync(file));
  });
  await new Promise(resolve => server.listen(0, "127.0.0.1", resolve));
  const origin = "http://127.0.0.1:" + server.address().port;
  let browser;
  const result = { checked_pages: [], viewport_widths: [320, 375, 1280], external_requests: [],
    javascript_errors: [], keyboard: "not_run", form: "not_run", no_javascript: "not_run",
    limits: ["Chromium seulement", "pas de lecteur d'écran", "pas de HTTPS/hébergeur réel"] };
  try {
    browser = await chromium.launch({headless: true});
    for (const width of result.viewport_widths) {
      const context = await browser.newContext({viewport: {width, height: 900}, serviceWorkers: "block"});
      await context.route("**/*", route => {
        if (new URL(route.request().url()).origin !== origin) {
          result.external_requests.push("requête externe bloquée");
          return route.abort();
        }
        return route.continue();
      });
      const page = await context.newPage();
      page.on("pageerror", error => result.javascript_errors.push(error.message));
      page.on("console", message => {
        if (message.type() === "error") result.javascript_errors.push(message.text());
      });
      for (const name of pages) {
        const response = await page.goto(origin + "/" + name);
        assert.equal(response.status(), 200);
        assert.equal(await page.locator("h1").count(), 1);
        assert.equal(await page.locator(".demo-banner").isVisible(), true);
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), true);
        result.checked_pages.push({name, width});
      }
      if (width === 375) {
        await page.goto(origin + "/index.html");
        await page.keyboard.press("Tab");
        assert.equal(await page.locator(".skip").evaluate(el => el === document.activeElement), true);
        await page.locator(".menu-btn").focus();
        await page.keyboard.press("Enter");
        assert.equal(await page.locator(".menu-btn").getAttribute("aria-expanded"), "true");
        await page.keyboard.press("Escape");
        assert.equal(await page.locator(".menu-btn").getAttribute("aria-expanded"), "false");
        result.keyboard = "passed";
        await page.goto(origin + "/contact.html");
        assert.equal(await page.locator("input:enabled, textarea:enabled, button[type=submit]:enabled").count(), 0);
        result.form = "passed";
      }
      await context.close();
    }
    const context = await browser.newContext({javaScriptEnabled: false, viewport: {width: 375, height: 900}});
    const page = await context.newPage();
    await page.goto(origin + "/index.html");
    assert.equal(await page.locator("#menu").isVisible(), true);
    assert.equal(await page.locator("#menu a").count(), 7);
    result.no_javascript = "passed";
    await context.close();
    assert.equal(result.external_requests.length, 0);
    assert.equal(result.javascript_errors.length, 0);
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error(JSON.stringify({status: "failed", reason: error.message, observed: result}, null, 2));
    process.exitCode = 1;
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
}
run().catch(error => { console.error(error.message); process.exitCode = 1; });
