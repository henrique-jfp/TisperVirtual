// components/StagingSidebar.tsx
'use client';

import { useState } from 'react';
import { useStagingDocuments, StagingDocument } from '@/hooks/useStagingDocuments';
import { ReviewModal } from './ReviewModal';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { FileText, Clock } from 'lucide-react';

/**
 * Sidebar que exibe uma lista de documentos pendentes de revisão.
 */
export function StagingSidebar() {
  const { documents, loading, error, refresh } = useStagingDocuments();
  const [selectedDoc, setSelectedDoc] = useState<StagingDocument | null>(null);

  const handleSelectDocument = (doc: StagingDocument) => {
    setSelectedDoc(doc);
  };

  const handleCloseModal = () => {
    setSelectedDoc(null);
    refresh(); // Atualiza a lista após o modal ser fechado
  };

  return (
    <aside className="w-80 border-r bg-gray-50/50 dark:bg-gray-900/50 h-full flex flex-col p-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold flex items-center gap-2">
          <FileText className="w-5 h-5" />
          <span>Para Revisão</span>
        </h2>
        {loading ? (
          <Badge variant="secondary" className="animate-pulse">...</Badge>
        ) : (
          <Badge className="bg-green-500 hover:bg-green-600 text-white text-sm px-2.5 py-1">
            {documents.length}
          </Badge>
        )}
      </div>
      
      {error && <p className="text-red-500 text-sm px-2">Erro ao carregar documentos.</p>}

      <ScrollArea className="flex-grow -mr-4 pr-4">
        <div className="space-y-2">
          {documents.map((doc) => (
            <div
              key={doc.id}
              onClick={() => handleSelectDocument(doc)}
              className="p-3 border rounded-lg cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors group"
            >
              <p className="font-medium truncate text-sm group-hover:text-primary">
                {doc.raw_data.title || 'Documento sem título'}
              </p>
              <div className="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400 mt-1">
                <Clock className="w-3 h-3" />
                <span>{new Date(doc.created_at).toLocaleString('pt-BR')}</span>
              </div>
            </div>
          ))}
          {!loading && documents.length === 0 && (
            <div className="text-center text-sm text-gray-500 py-10">
              Nenhum documento pendente.
            </div>
          )}
        </div>
      </ScrollArea>

      {/* O Modal de Revisão será renderizado aqui quando um documento for selecionado */}
      {selectedDoc && (
        <ReviewModal
          document={selectedDoc}
          onClose={handleCloseModal}
        />
      )}
    </aside>
  );
}
