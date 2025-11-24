// app/api/approve-document/route.ts
import { createClient } from '@/lib/supabase/server';
import { NextRequest, NextResponse } from 'next/server';

/**
 * API Route para aprovar um documento.
 * 1. Insere os dados revisados na tabela final 'documents'.
 * 2. Deleta (ou atualiza o status) do registro na tabela 'staging_documents'.
 */
export async function POST(request: NextRequest) {
  // Usamos o cliente de servidor para operações seguras
  const supabase = await createClient();

  // Validar se o usuário está autenticado
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) {
    return NextResponse.json({ error: 'Não autorizado' }, { status: 401 });
  }

  try {
    const { stagingId, content, metadata } = await request.json();

    if (!stagingId || !content || !metadata) {
      return NextResponse.json({ error: 'Dados incompletos fornecidos.' }, { status: 400 });
    }

    // Passo 1: Inserir na tabela oficial 'documents'
    // Aqui é onde a geração de embedding deve acontecer.
    // Por simplicidade, vamos assumir que a geração é feita por um trigger no DB
    // ou que será adicionada posteriormente.
    const { error: insertError } = await supabase
      .from('documents') // Sua tabela final com pgvector
      .insert({
        content: content,
        metadata: metadata,
        // embedding: '...', // O vetor seria inserido aqui
        user_id: user.id
      });

    if (insertError) {
      console.error('Supabase insert error:', insertError);
      throw new Error(`Falha ao inserir na tabela final: ${insertError.message}`);
    }

    // Passo 2: Deletar o registro da tabela de staging para evitar reprocessamento
    const { error: deleteError } = await supabase
      .from('staging_documents')
      .delete()
      .eq('id', stagingId);

    if (deleteError) {
      // CRÍTICO: O dado já foi inserido, mas a limpeza falhou.
      // Logar este erro é vital para reconciliação manual.
      console.error(
        `CRITICAL: Failed to delete staging document (id: ${stagingId}) after approval. Manual cleanup required.`,
        deleteError
      );
      // Não lançamos um erro para o cliente, pois a operação principal (inserção) foi bem-sucedida.
    }

    return NextResponse.json({ success: true, message: 'Documento aprovado e salvo com sucesso.' }, { status: 200 });

  } catch (error: any) {
    console.error('[API Approve Error]:', error);
    return NextResponse.json({ error: error.message || 'Erro interno do servidor.' }, { status: 500 });
  }
}
