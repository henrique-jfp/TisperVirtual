// components/ReviewModal.tsx
'use client';

import { useState } from 'react';
import { StagingDocument } from '@/hooks/useStagingDocuments';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogDescription } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';

interface ReviewModalProps {
  document: StagingDocument;
  onClose: () => void;
}

/**
 * Modal para revisar, editar e aprovar um documento extraído.
 */
export function ReviewModal({ document, onClose }: ReviewModalProps) {
  // Estado para o conteúdo editável
  const [markdown, setMarkdown] = useState(document.raw_data.editable_markdown || '');
  
  // Estado para os metadados editáveis
  const [metadata, setMetadata] = useState({
    title: document.raw_data.title || '',
    teams: document.raw_data.teams?.join(', ') || '',
    score: document.raw_data.score || '',
    date: document.raw_data.date ? new Date(document.raw_data.date).toISOString().substring(0, 16) : '', // Formato para datetime-local
    competition: document.raw_data.competition || '',
  });

  const [isSaving, setIsSaving] = useState(false);

  const handleMetadataChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setMetadata(prev => ({ ...prev, [name]: value }));
  };

  const handleConfirmAndSave = async () => {
    setIsSaving(true);
    const toastId = toast.loading('Salvando documento...');
    
    const finalData = {
      stagingId: document.id,
      content: markdown,
      metadata: {
        ...metadata,
        teams: metadata.teams.split(',').map(t => t.trim()).filter(Boolean),
        date: metadata.date ? new Date(metadata.date).toISOString() : null, // Converte de volta para ISO string
        source_url: document.raw_data.source_url
      },
    };

    try {
      const response = await fetch('/api/approve-document', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(finalData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Falha ao salvar o documento.');
      }

      toast.success('Documento salvo com sucesso!', { id: toastId });
      onClose();

    } catch (error: any) {
      console.error('Error confirming document:', error);
      toast.error(`Erro: ${error.message}`, { id: toastId });
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent className="max-w-6xl h-[90vh] flex flex-col bg-white dark:bg-gray-900">
        <DialogHeader>
          <DialogTitle>Revisão de Documento Extraído</DialogTitle>
          <DialogDescription>
            Ajuste o conteúdo e os metadados antes de salvar na base de conhecimento.
          </DialogDescription>
        </DialogHeader>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 flex-grow overflow-hidden py-4">
          {/* Coluna Esquerda: Editor de Markdown */}
          <div className="flex flex-col h-full">
            <Label htmlFor="markdown-editor" className="mb-2 font-semibold">Conteúdo (Markdown)</Label>
            <Textarea
              id="markdown-editor"
              value={markdown}
              onChange={(e) => setMarkdown(e.target.value)}
              className="flex-grow resize-none text-base"
              placeholder="Conteúdo extraído da página..."
            />
          </div>

          {/* Coluna Direita: Metadados */}
          <div className="flex flex-col space-y-4 overflow-y-auto pr-4">
            <h3 className="font-semibold mb-2">Metadados</h3>
            <div className="space-y-2">
              <Label htmlFor="title">Título</Label>
              <Input id="title" name="title" value={metadata.title} onChange={handleMetadataChange} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="teams">Times (separados por vírgula)</Label>
              <Input id="teams" name="teams" value={metadata.teams} onChange={handleMetadataChange} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="score">Placar</Label>
              <Input id="score" name="score" value={metadata.score} onChange={handleMetadataChange} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="date">Data e Hora</Label>
              <Input id="date" name="date" type="datetime-local" value={metadata.date} onChange={handleMetadataChange} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="competition">Competição</Label>
              <Input id="competition" name="competition" value={metadata.competition} onChange={handleMetadataChange} />
            </div>
          </div>
        </div>

        <DialogFooter className="mt-4 pt-4 border-t">
          <Button variant="outline" onClick={onClose} disabled={isSaving}>Cancelar</Button>
          <Button onClick={handleConfirmAndSave} disabled={isSaving}>
            {isSaving ? 'Salvando...' : 'Confirmar e Salvar'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
