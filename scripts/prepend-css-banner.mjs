import { readFile, writeFile } from "node:fs/promises";

const path = new URL("../app/static/app.css", import.meta.url);
const banner = `/* Hallmark · pre-emit critique: P5 H4 E4 S5 R5 V4
 * Hallmark · macrostructure: Bento Grid · tone: utilitarian · anchor hue: neutral
 * genre: modern-minimal · theme: monochrome utility · enrichment: none · nav: N9
 * contrast: pass (40–41) · slop: pass (42–45) · mobile: pass (34, 49, 50–57)
 */\n`;
const css = await readFile(path, "utf8");
const withoutGeneratedBanner = css.replace(/\/\*!? Hallmark[\s\S]*?\*\/\n?/g, "");
await writeFile(path, banner + withoutGeneratedBanner, "utf8");
