// hooks/useStagingDocuments.ts
'use client';

import { useState, useEffect, useCallback } from 'react';

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
  const [documents, setDocuments] = useState<StagingDocument[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDocuments = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await fetch('/api/staging-documents');
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const payload = await r.json();
      setDocuments((payload.data || []) as StagingDocument[]);
    } catch (e: any) {
      console.error('Error fetching staging documents:', e);
      setError(e.message || String(e));
      setDocuments([]);
    } finally {
      setLoading(false);
    }
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
