// Deprecated: Remote favicon service now used directly; keeping script for reference.
import fs from 'node:fs/promises';
import path from 'node:path';
import https from 'node:https';

const outDir = path.resolve(process.cwd(), 'public/providers');
await fs.mkdir(outDir, { recursive: true });

// Keep in sync with Providers.astro list
const providers = [
  { name:'OpenAI', domain:'openai.com', file:'openai.ico' },
  { name:'Groq', domain:'groq.com', file:'groq.ico' },
  { name:'Anthropic', domain:'anthropic.com', file:'anthropic.ico' },
  { name:'Gemini', domain:'gemini.google.com', file:'gemini.ico' },
  { name:'Mistral', domain:'mistral.ai', file:'mistral.ico' },
  { name:'Cohere', domain:'cohere.com', file:'cohere.ico' },
  { name:'HuggingFace', domain:'huggingface.co', file:'huggingface.ico' },
  { name:'TogetherAI', domain:'together.ai', file:'togetherai.ico' },
  { name:'DeepSeek', domain:'deepseek.com', file:'deepseek.ico' },
  { name:'Qwen', domain:'qwen.ai', file:'qwen.ico' },
  { name:'Baidu Wenxin', domain:'baidu.com', file:'baidu.ico' },
  { name:'Tencent Hunyuan', domain:'hunyuan.tencent.com', file:'hunyuan.ico' },
  { name:'iFlytek Spark', domain:'xfyun.cn', file:'iflytek.ico' },
  { name:'Moonshot Kimi', domain:'moonshot.cn', file:'kimi.ico' },
  { name:'Azure OpenAI', domain:'azure.microsoft.com', file:'azure.ico' },
  { name:'Ollama', domain:'ollama.com', file:'ollama.ico' },
  { name:'xAI Grok', domain:'x.ai', file:'grok.ico' }
];

function fetchFile(url, dest){
  return new Promise((resolve, reject) => {
    https.get(url, res => {
      if(res.statusCode && res.statusCode >= 300 && res.statusCode < 400 && res.headers.location){
        // handle redirect
        return fetchFile(res.headers.location, dest).then(resolve, reject);
      }
      if(res.statusCode !== 200){
        res.resume();
        return reject(new Error('HTTP '+res.statusCode+' for '+url));
      }
      const data=[];
      res.on('data',d=>data.push(d));
      res.on('end',()=>{
        fs.writeFile(dest, Buffer.concat(data)).then(()=>resolve(), reject);
      });
    }).on('error', reject);
  });
}

for (const p of providers){
  const target = path.join(outDir, p.file);
  try {
    await fs.access(target);
    console.log('Exists', p.file);
    continue;
  } catch {}
  const faviconUrl = `https://${p.domain.replace(/\/$/, '')}/favicon.ico`;
  try {
    await fetchFile(faviconUrl, target);
    console.log('Fetched', p.name, '->', p.file);
  } catch (e){
    console.warn('Failed', p.name, faviconUrl, e.message);
  }
}
