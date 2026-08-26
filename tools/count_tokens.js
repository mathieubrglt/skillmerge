// Token counting CLI. Reads JSON {"texts": [...]} on stdin, writes {"anthropic":[...], "o200k":[...]}
const { countTokens } = require('@anthropic-ai/tokenizer');
const gpt = require('gpt-tokenizer');
let buf = '';
process.stdin.on('data', d => buf += d);
process.stdin.on('end', () => {
  const { texts } = JSON.parse(buf);
  const out = { anthropic: [], o200k: [] };
  for (const t of texts) { out.anthropic.push(countTokens(t)); out.o200k.push(gpt.encode(t).length); }
  process.stdout.write(JSON.stringify(out));
});
