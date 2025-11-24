// app/api/staging-documents/route.ts
import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

const DATA_DIR = path.join(process.cwd(), 'frontend_next', 'data');
const STAGING_FILE = path.join(DATA_DIR, 'staging_documents.json');

function ensureDataDir() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
  if (!fs.existsSync(STAGING_FILE)) fs.writeFileSync(STAGING_FILE, '[]', 'utf-8');
}

export async function GET() {
  try {
    ensureDataDir();
    const raw = fs.readFileSync(STAGING_FILE, 'utf-8');
    const arr = JSON.parse(raw || '[]');
    // return only pending_review ordered by created_at desc
    const pending = (arr.filter((r: any) => r.status === 'pending_review') as any[])
      .sort((a, b) => (b.created_at || '').localeCompare(a.created_at || ''));
    return NextResponse.json({ data: pending }, { status: 200 });
  } catch (err: any) {
    console.error('[API staging-documents GET] error:', err);
    return NextResponse.json({ error: err.message || String(err) }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    ensureDataDir();
    const body = await request.json();
    const raw_data = body.raw_data;

    if (!raw_data) {
      return NextResponse.json({ error: 'raw_data is required' }, { status: 400 });
    }

    const now = new Date().toISOString();
    const newDoc = {
      id: String(Math.floor(Math.random() * 1e12)),
      raw_data,
      status: 'pending_review',
      created_at: now,
    };

    const raw = fs.readFileSync(STAGING_FILE, 'utf-8');
    const arr = JSON.parse(raw || '[]');
    arr.push(newDoc);
    fs.writeFileSync(STAGING_FILE, JSON.stringify(arr, null, 2), 'utf-8');

    return NextResponse.json({ success: true, document: newDoc }, { status: 200 });
  } catch (err: any) {
    console.error('[API staging-documents POST] error:', err);
    return NextResponse.json({ error: err.message || String(err) }, { status: 500 });
  }
}
