import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://shubham-anil-gade.github.io',
  output: 'static',
  build: {
    format: 'directory'
  }
});
