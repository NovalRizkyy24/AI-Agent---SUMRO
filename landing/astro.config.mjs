import { defineConfig } from 'astro/config';

// Di Vercel, alamat produksi diambil otomatis; lokal memakai localhost.
const vercelHost = process.env.VERCEL_PROJECT_PRODUCTION_URL;

export default defineConfig({
  site: vercelHost ? `https://${vercelHost}` : 'http://localhost:4321',
});
