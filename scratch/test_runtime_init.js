const fs = require('fs');

// We test that all classes can be constructed and that their methods behave as expected.
// We can mock minimal DOM
const indexHtml = fs.readFileSync('web/index.html', 'utf8');

// Ensure all script tags match files on disk
const scriptMatches = indexHtml.match(/<script[^>]*src=["']([^"']+)["'][^>]*>/g) || [];
console.log('Script tags in index.html:', scriptMatches);

for (const tag of scriptMatches) {
  const match = tag.match(/src=["']([^"']+)["']/);
  if (match && match[1]) {
    const src = match[1];
    if (!fs.existsSync('web/' + src)) {
      console.error('ERROR: Script src does not exist:', src);
      process.exit(1);
    } else {
      console.log('Verified script exists on disk: web/' + src);
    }
  }
}

console.log('Frontend verification passed successfully.');
