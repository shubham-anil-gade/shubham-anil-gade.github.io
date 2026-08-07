export async function GET() {
  const xml = `<?xml version="1.0" encoding="UTF-8" ?>
  <rss version="2.0"><channel>
    <title>Shubham Gade — Posts</title>
    <link>https://shubham-anil-gade.github.io/posts/</link>
    <description>Research notes, technical insights and field perspectives from Shubham Gade.</description>
    <language>en</language>
  </channel></rss>`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml' } });
}
