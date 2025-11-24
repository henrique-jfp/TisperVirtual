// app/api/staging-documents/route.ts
import { createClient } from '@/lib/supabase/server';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const supabase = await createClient();

    const body = await request.json();
    const raw_data = body.raw_data;

    if (!raw_data) {
      return NextResponse.json({ error: 'raw_data is required' }, { status: 400 });
    }

    const { data, error } = await supabase
      .from('staging_documents')
      .insert([{ raw_data, status: 'pending_review' }])
      .select()
      .single();

    if (error) {
      console.error('[API staging-documents] insert error:', error);
      return NextResponse.json({ error: error.message || 'DB error' }, { status: 500 });
    }

    return NextResponse.json({ success: true, document: data }, { status: 200 });
  } catch (err: any) {
    console.error('[API staging-documents] error:', err);
    return NextResponse.json({ error: err.message || String(err) }, { status: 500 });
  }
}
