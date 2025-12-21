import { QdrantClient } from '@qdrant/js-client-rest';
import dotenv from 'dotenv';
import OpenAI from 'openai';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Initialize clients
const qdrantClient = new QdrantClient({
  url: process.env.QDRANT_URL,
  apiKey: process.env.QDRANT_API_KEY,
});

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

const COLLECTION_NAME = 'docusaurus-content';

async function createCollection() {
  try {
    // Check if collection already exists
    const collections = await qdrantClient.getCollections();
    const collectionExists = collections.collections.some(
      collection => collection.name === COLLECTION_NAME
    );

    if (!collectionExists) {
      await qdrantClient.createCollection(COLLECTION_NAME, {
        vectors: {
          size: 1536, // OpenAI embedding dimension
          distance: 'Cosine',
        },
      });
      console.log(`Collection ${COLLECTION_NAME} created successfully.`);
    } else {
      console.log(`Collection ${COLLECTION_NAME} already exists.`);
    }
  } catch (error) {
    console.error('Error creating collection:', error);
    throw error;
  }
}

async function getEmbedding(text) {
  try {
    const response = await openai.embeddings.create({
      model: 'text-embedding-ada-002',
      input: text.replace(/\s+/g, ' ').trim(),
    });

    return response.data[0].embedding;
  } catch (error) {
    console.error('Error getting embedding:', error);
    throw error;
  }
}

function extractTextFromMarkdown(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');

  // Remove markdown formatting and extract plain text
  let plainText = content
    // Remove code blocks
    .replace(/```[\s\S]*?```/g, '')
    // Remove inline code
    .replace(/`[^`]*`/g, '')
    // Remove markdown headers, links, bold, italic
    .replace(/#{1,6}\s*(.+?)\n/g, '$1 ')
    .replace(/\[(.+?)\]\(.+?\)/g, '$1')
    .replace(/\*\*(.+?)\*\*/g, '$1')
    .replace(/\*(.+?)\*/g, '$1')
    .replace(/__.+?__/g, '$1')
    .replace(/_.+?_/g, '$1')
    .replace(/!\[.*?\]\(.*?\)/g, '')
    .replace(/---\n[\s\S]*?\n---/g, ''); // Remove frontmatter

  return plainText.trim();
}

function chunkText(text, maxLength = 1000) {
  const chunks = [];
  const paragraphs = text.split('\n\n').filter(p => p.trim() !== '');

  let currentChunk = '';

  for (const paragraph of paragraphs) {
    if ((currentChunk + paragraph).length > maxLength) {
      if (currentChunk.length > 0) {
        chunks.push(currentChunk.trim());
        currentChunk = paragraph + '\n\n';
      } else {
        // If a single paragraph is too long, split it by sentences
        const sentences = paragraph.match(/[^\.!?]+[\.!?]+/g) || [paragraph];
        let tempChunk = '';

        for (const sentence of sentences) {
          if ((tempChunk + sentence).length > maxLength) {
            if (tempChunk.length > 0) {
              chunks.push(tempChunk.trim());
              tempChunk = sentence + ' ';
            } else {
              // If a single sentence is too long, split by length
              const sentenceChunks = sentence.match(new RegExp(`.{1,${maxLength}}`, 'g')) || [sentence];
              chunks.push(sentenceChunks[0].trim());
              tempChunk = sentenceChunks.slice(1).join('');
            }
          } else {
            tempChunk += sentence + ' ';
          }
        }

        if (tempChunk.length > 0) {
          if (tempChunk.length > maxLength) {
            const tempChunks = tempChunk.match(new RegExp(`.{1,${maxLength}}`, 'g')) || [tempChunk];
            chunks.push(tempChunks[0].trim());
          } else {
            currentChunk = tempChunk;
          }
        }
      }
    } else {
      currentChunk += paragraph + '\n\n';
    }
  }

  if (currentChunk.length > 0) {
    chunks.push(currentChunk.trim());
  }

  return chunks.filter(chunk => chunk.length > 0);
}

async function ingestDocument(filePath, source) {
  try {
    const content = extractTextFromMarkdown(filePath);
    const chunks = chunkText(content, 1000); // 1000 character chunks

    console.log(`Processing ${chunks.length} chunks from ${source}`);

    for (let i = 0; i < chunks.length; i++) {
      const chunk = chunks[i];

      if (chunk.length < 10) continue; // Skip very short chunks

      console.log(`Processing chunk ${i + 1}/${chunks.length} (${chunk.length} chars)`);

      // Generate embedding
      const embedding = await getEmbedding(chunk);

      // Upsert to Qdrant
      await qdrantClient.upsert(COLLECTION_NAME, {
        wait: true,
        points: [
          {
            id: `${source}_${i}`,
            vector: embedding,
            payload: {
              content: chunk,
              source: source,
              chunk_index: i,
              timestamp: new Date().toISOString(),
            },
          },
        ],
      });
    }

    console.log(`Successfully ingested ${source}`);
  } catch (error) {
    console.error(`Error ingesting ${source}:`, error);
    throw error;
  }
}

async function scanAndIngestDocs(docsDir) {
  const files = [];

  function walk(dir) {
    const dirents = fs.readdirSync(dir);
    for (const dirent of dirents) {
      const fullPath = path.join(dir, dirent);
      const stat = fs.statSync(fullPath);

      if (stat.isDirectory()) {
        walk(fullPath);
      } else if (fullPath.endsWith('.md') || fullPath.endsWith('.mdx')) {
        files.push(fullPath);
      }
    }
  }

  walk(docsDir);

  console.log(`Found ${files.length} markdown files to process`);

  for (const file of files) {
    const relativePath = path.relative(docsDir, file);
    await ingestDocument(file, relativePath);
  }
}

async function main() {
  console.log('Starting ingestion process...');

  // Create collection if it doesn't exist
  await createCollection();

  // Look for Docusaurus docs in common locations
  const possibleDocPaths = [
    '../physical-ai-textbook/docs',
    '../physical-ai-textbook/src/pages',
    '../physical-ai-textbook/blog',
    '../docs',
    '../source'
  ];

  let docsFound = false;

  for (const docsPath of possibleDocPaths) {
    const fullPath = path.resolve(__dirname, docsPath);
    if (fs.existsSync(fullPath)) {
      console.log(`Found docs directory: ${fullPath}`);
      await scanAndIngestDocs(fullPath);
      docsFound = true;
      break;
    }
  }

  if (!docsFound) {
    console.warn('No Docusaurus docs directory found. Looking for markdown files in parent directory...');

    // Fallback: look for markdown files in the parent directory
    const parentDir = path.resolve(__dirname, '..');
    const mdFiles = fs.readdirSync(parentDir).filter(file =>
      (file.endsWith('.md') || file.endsWith('.mdx')) &&
      !file.startsWith('.') &&
      !file.startsWith('node_modules')
    );

    if (mdFiles.length > 0) {
      console.log(`Found ${mdFiles.length} markdown files in parent directory`);
      for (const mdFile of mdFiles) {
        const fullPath = path.join(parentDir, mdFile);
        await ingestDocument(fullPath, mdFile);
      }
    } else {
      console.error('No markdown files found to ingest. Please check your Docusaurus docs location.');
      return;
    }
  }

  console.log('Ingestion process completed successfully!');
}

if (process.argv[1] === __filename) {
  main().catch(console.error);
}

export { ingestDocument, createCollection };