// hooks/useStagingDocuments.ts
'use client';

import { useState, useEffect, useCallback } from 'react';
import { createClient } from '@/lib/supabase/client';

// Define o tipo de dado esperado da tabela de rascunhos
export interface StagingDocument {
  id: string;
  raw_data: {
    title: string;
    editable_markdown: string;
    source_url?: string;
    teams?: string[];
    score?: string;
    date?: string;
    competition?: string;
  };
  status: 'pending_review' | 'approved' | 'rejected';
  created_at: string;
}

/**
 * Hook customizado para buscar e gerenciar documentos pendentes de revisão.
 */
export function useStagingDocuments() {
  const supabase = createClient();
  const [documents, setDocuments] = useState<StagingDocument[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDocuments = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    const { data, error } = await supabase
      .from('staging_documents')
      .select('*')
      .eq('status', 'pending_review')
      .order('created_at', { ascending: false });

    if (error) {
      console.error('Error fetching staging documents:', error);
      setError(error.message);
      setDocuments([]);
    } else {
      // O Supabase retorna os dados, mas precisamos garantir que eles correspondam à nossa interface
      setDocuments(data as StagingDocument[]);
    }
    setLoading(false);
  }, [supabase]);

  useEffect(() => {
    fetchDocuments();
    const onStagingChanged = () => {
      fetchDocuments();
    };
    window.addEventListener('staging:changed', onStagingChanged);
    return () => {
      window.removeEventListener('staging:changed', onStagingChanged);
    };
  }, [fetchDocuments]);

  // Expõe a lista, o estado de carregamento/erro e uma função para atualizar
  return { documents, loading, error, refresh: fetchDocuments };
}
