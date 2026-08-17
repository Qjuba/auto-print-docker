import { copyFile, mkdir, rm } from "node:fs/promises";

const source = new URL("../node_modules/@fontsource-variable/geist/files/", import.meta.url);
const destination = new URL("../app/static/fonts/", import.meta.url);
await mkdir(destination, { recursive: true });
for (const name of ["public-sans-latin-ext-wght-normal.woff2", "public-sans-latin-wght-normal.woff2"]) {
  await rm(new URL(name, destination), { force: true });
}
for (const name of ["geist-latin-ext-wght-normal.woff2", "geist-latin-wght-normal.woff2"]) {
  await copyFile(new URL(name, source), new URL(name, destination));
}
