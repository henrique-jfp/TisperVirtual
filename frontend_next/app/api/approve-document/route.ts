// app/api/approve-document/route.ts
import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

const DATA_DIR = path.join(process.cwd(), 'frontend_next', 'data');
const STAGING_FILE = path.join(DATA_DIR, 'staging_documents.json');
const DOCS_FILE = path.join(DATA_DIR, 'documents.json');

function ensureDataDir() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
  if (!fs.existsSync(STAGING_FILE)) fs.writeFileSync(STAGING_FILE, '[]', 'utf-8');
  if (!fs.existsSync(DOCS_FILE)) fs.writeFileSync(DOCS_FILE, '[]', 'utf-8');
}

export async function POST(request: NextRequest) {
  try {
    ensureDataDir();
    const { stagingId, content, metadata } = await request.json();

    if (!stagingId || !content || !metadata) {
      return NextResponse.json({ error: 'Dados incompletos fornecidos.' }, { status: 400 });
    }

    const stagingRaw = fs.readFileSync(STAGING_FILE, 'utf-8');
    const stagingArr = JSON.parse(stagingRaw || '[]');

    const idx = stagingArr.findIndex((r: any) => String(r.id) === String(stagingId));
    if (idx === -1) {
      return NextResponse.json({ error: 'Staging document not found' }, { status: 404 });
    }

    const doc = {
      id: String(Math.floor(Math.random() * 1e12)),
      content,
      metadata,
      created_at: new Date().toISOString(),
    };

    const docsRaw = fs.readFileSync(DOCS_FILE, 'utf-8');
    const docsArr = JSON.parse(docsRaw || '[]');
    docsArr.push(doc);
    fs.writeFileSync(DOCS_FILE, JSON.stringify(docsArr, null, 2), 'utf-8');

    // Remove from staging
    stagingArr.splice(idx, 1);
    fs.writeFileSync(STAGING_FILE, JSON.stringify(stagingArr, null, 2), 'utf-8');

    return NextResponse.json({ success: true, message: 'Documento aprovado e salvo com sucesso.' }, { status: 200 });
  } catch (error: any) {
    console.error('[API Approve Error]:', error);
    return NextResponse.json({ error: error.message || 'Erro interno do servidor.' }, { status: 500 });
  }
}
