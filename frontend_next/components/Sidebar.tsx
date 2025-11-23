import React, { useState, useEffect } from 'react'
import { Upload, FileText, Trash2, Plus, File, BarChart3, Calendar, Code, HelpCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from '@/components/ui/alert-dialog'
import { toast } from 'sonner'

interface Document {
  id: string
  name: string
  type: 'pdf' | 'markdown' | 'csv' | 'json' | 'ics' | 'yaml'
  date: string
  status: 'processed' | 'processing'
}

export default function Sidebar() {
  const [documents, setDocuments] = useState<Document[]>([])
  const [manualDialogOpen, setManualDialogOpen] = useState(false)
  const [manualTitle, setManualTitle] = useState('')
  const [manualText, setManualText] = useState('')
  const [manualCategory, setManualCategory] = useState('')

  useEffect(() => {
    // fetchDocuments() // Temporariamente desabilitado - API não implementada
  }, [])

  const fetchDocuments = async () => {
    try {
      // const res = await fetch('http://127.0.0.1:8000/api/documents')
      // const data = await res.json()
      // setDocuments(data?.documents || [])
      setDocuments([]) // Lista vazia por enquanto
    } catch (err) {
      console.error('Error fetching documents:', err)
      setDocuments([])
    }
  }

  const handleFileUpload = async (files: FileList | null, category: string) => {
    if (!files) return
    for (const file of Array.from(files)) {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('category', category) // Adicionar categoria para backend futuro
      
      try {
        const res = await fetch('http://127.0.0.1:8000/api/upload', {
          method: 'POST',
          body: formData
        })
        const data = await res.json()
        if (res.ok) {
          toast.success(data.message)
          setDocuments(prev => [...prev, data.document])
        } else {
          toast.error(data.detail || 'Upload failed')
        }
      } catch (err) {
        toast.error('Error uploading file')
        console.error(err)
      }
    }
  }

  const deleteDocument = async (id: string) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/documents/${id}`, {
        method: 'DELETE'
      })
      if (res.ok) {
        setDocuments(prev => prev.filter(doc => doc.id !== id))
        toast.success('Documento deletado!')
      } else {
        toast.error('Error deleting document')
      }
    } catch (err) {
      toast.error('Error deleting document')
      console.error(err)
    }
  }

  const handleManualSubmit = async () => {
    if (!manualTitle.trim() || !manualText.trim() || !manualCategory) return
    try {
      const res = await fetch('http://127.0.0.1:8000/api/manual', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ titulo: manualTitle, texto: manualText, categoria: manualCategory })
      })
      const data = await res.json()
      if (res.ok) {
        toast.success(data.message)
        setDocuments(prev => [...prev, data.document])
        setManualDialogOpen(false)
        setManualTitle('')
        setManualText('')
        setManualCategory('')
      } else {
        toast.error(data.detail || 'Erro ao adicionar nota')
      }
    } catch (err) {
      toast.error('Erro ao adicionar nota')
      console.error(err)
    }
  }

  return (
    <aside className="w-1/4 bg-gradient-to-b from-gray-900 to-gray-800 text-white p-6 flex flex-col h-full overflow-auto">
      <div className="space-y-3 flex-1">
        {/* Livros e TCCs */}
        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-3">
            <div
              className="border-2 border-dashed border-gray-600 rounded-lg p-2 text-center hover:border-blue-500 transition-colors cursor-pointer"
              onDrop={(e) => {
                e.preventDefault()
                handleFileUpload(e.dataTransfer.files, 'livros')
              }}
              onDragOver={(e) => e.preventDefault()}
            >
              <FileText className="mx-auto h-5 w-5 text-gray-400 mb-1" />
              <div className="flex items-center justify-center mb-1">
                <p className="text-xs text-gray-300">Livros/TCCs</p>
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <HelpCircle className="h-4 w-4 ml-2 text-gray-400 hover:text-white cursor-help" />
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Formato ideal: Markdown (.md) para estrutura preservada. PDF suportado, mas converta para melhor compreensão da IA.</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </div>
              <p className="text-xs text-gray-400">PDFs, Markdowns</p>
              <input
                type="file"
                accept=".pdf,.md"
                multiple
                className="hidden"
                id="livros-upload"
                onChange={(e) => handleFileUpload(e.target.files, 'livros')}
              />
              <label htmlFor="livros-upload" className="text-blue-400 underline cursor-pointer text-xs">Selecionar</label>
            </div>
          </CardContent>
        </Card>

        {/* Estatísticas */}
        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-3">
            <div
              className="border-2 border-dashed border-gray-600 rounded-lg p-2 text-center hover:border-green-500 transition-colors cursor-pointer"
              onDrop={(e) => {
                e.preventDefault()
                handleFileUpload(e.dataTransfer.files, 'estatisticas')
              }}
              onDragOver={(e) => e.preventDefault()}
            >
              <BarChart3 className="mx-auto h-5 w-5 text-gray-400 mb-1" />
              <div className="flex items-center justify-center mb-1">
                <p className="text-xs text-gray-300">Estatísticas</p>
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <HelpCircle className="h-4 w-4 ml-2 text-gray-400 hover:text-white cursor-help" />
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Formato ideal: CSV ou JSON para dados estruturados. Facilita análise e consultas da IA.</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </div>
              <p className="text-xs text-gray-400">CSVs, JSONs</p>
              <input
                type="file"
                accept=".csv,.json"
                multiple
                className="hidden"
                id="estatisticas-upload"
                onChange={(e) => handleFileUpload(e.target.files, 'estatisticas')}
              />
              <label htmlFor="estatisticas-upload" className="text-green-400 underline cursor-pointer text-xs">Selecionar</label>
            </div>
          </CardContent>
        </Card>

        {/* Calendários */}
        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-3">
            <div
              className="border-2 border-dashed border-gray-600 rounded-lg p-2 text-center hover:border-red-500 transition-colors cursor-pointer"
              onDrop={(e) => {
                e.preventDefault()
                handleFileUpload(e.dataTransfer.files, 'calendarios')
              }}
              onDragOver={(e) => e.preventDefault()}
            >
              <Calendar className="mx-auto h-5 w-5 text-gray-400 mb-1" />
              <div className="flex items-center justify-center mb-1">
                <p className="text-xs text-gray-300">Calendários</p>
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <HelpCircle className="h-4 w-4 ml-2 text-gray-400 hover:text-white cursor-help" />
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Formato ideal: ICS (.ics) para eventos de calendário. CSV suportado para listas simples.</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </div>
              <p className="text-xs text-gray-400">.ics, CSVs</p>
              <input
                type="file"
                accept=".ics,.csv"
                multiple
                className="hidden"
                id="calendarios-upload"
                onChange={(e) => handleFileUpload(e.target.files, 'calendarios')}
              />
              <label htmlFor="calendarios-upload" className="text-red-400 underline cursor-pointer text-xs">Selecionar</label>
            </div>
          </CardContent>
        </Card>

        {/* Documentos de API */}
        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-3">
            <div
              className="border-2 border-dashed border-gray-600 rounded-lg p-2 text-center hover:border-indigo-500 transition-colors cursor-pointer"
              onDrop={(e) => {
                e.preventDefault()
                handleFileUpload(e.dataTransfer.files, 'apis')
              }}
              onDragOver={(e) => e.preventDefault()}
            >
              <Code className="mx-auto h-5 w-5 text-gray-400 mb-1" />
              <div className="flex items-center justify-center mb-1">
                <p className="text-xs text-gray-300">APIs</p>
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <HelpCircle className="h-4 w-4 ml-2 text-gray-400 hover:text-white cursor-help" />
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Formato ideal: Markdown (.md) para documentação, JSON/YAML para specs de API. Facilita integração e consultas.</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </div>
              <p className="text-xs text-gray-400">MDs, JSONs, YAMLs</p>
              <input
                type="file"
                accept=".md,.json,.yaml,.yml"
                multiple
                className="hidden"
                id="apis-upload"
                onChange={(e) => handleFileUpload(e.target.files, 'apis')}
              />
              <label htmlFor="apis-upload" className="text-indigo-400 underline cursor-pointer text-xs">Selecionar</label>
            </div>
          </CardContent>
        </Card>

        {/* Documentos Processados */}
        <Card className="bg-gray-800 border-gray-700 flex-1">
          <CardHeader>
            <CardTitle className="text-white flex items-center justify-between">
              <span className="flex items-center">
                <FileText className="mr-2 h-5 w-5" />
                Documentos Processados
              </span>
              <span className="bg-green-600 text-xs px-2 py-1 rounded-full">{documents?.length || 0}</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ScrollArea className="h-48">
              <div className="space-y-2">
                {documents.map(doc => (
                  <div key={doc.id} className="bg-gray-700 p-3 rounded-lg hover:bg-gray-600 transition-colors flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      {doc.type === 'pdf' ? <FileText className="h-4 w-4 text-red-400" /> :
                       doc.type === 'markdown' ? <File className="h-4 w-4 text-blue-400" /> :
                       doc.type === 'csv' ? <BarChart3 className="h-4 w-4 text-green-400" /> :
                       doc.type === 'json' ? <Code className="h-4 w-4 text-yellow-400" /> :
                       doc.type === 'ics' ? <Calendar className="h-4 w-4 text-red-400" /> :
                       <Code className="h-4 w-4 text-pink-400" />}
                      <div>
                        <TooltipProvider>
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <p className="text-sm font-medium truncate max-w-32">{doc.name}</p>
                            </TooltipTrigger>
                            <TooltipContent>
                              <p>{doc.name}</p>
                            </TooltipContent>
                          </Tooltip>
                        </TooltipProvider>
                        <p className="text-xs text-gray-400">{doc.date}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className={`text-xs px-2 py-1 rounded-full ${doc.status === 'processed' ? 'bg-green-600' : 'bg-yellow-600'}`}>
                        {doc.status === 'processed' ? 'Processado' : 'Processando'}
                      </span>
                      <AlertDialog>
                        <AlertDialogTrigger asChild>
                          <Button variant="ghost" size="sm" className="text-red-400 hover:text-red-300">
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </AlertDialogTrigger>
                        <AlertDialogContent>
                          <AlertDialogHeader>
                            <AlertDialogTitle>Confirmar exclusão</AlertDialogTitle>
                            <AlertDialogDescription>
                              Tem certeza que deseja deletar "{doc.name}"? Esta ação não pode ser desfeita.
                            </AlertDialogDescription>
                          </AlertDialogHeader>
                          <AlertDialogFooter>
                            <AlertDialogCancel>Cancelar</AlertDialogCancel>
                            <AlertDialogAction onClick={() => deleteDocument(doc.id)}>Deletar</AlertDialogAction>
                          </AlertDialogFooter>
                        </AlertDialogContent>
                      </AlertDialog>
                    </div>
                  </div>
                ))}
              </div>
            </ScrollArea>
          </CardContent>
        </Card>

        {/* Criar Nota Manual */}
        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-3">
            <Dialog open={manualDialogOpen} onOpenChange={setManualDialogOpen}>
              <DialogTrigger asChild>
                <Button className="w-full bg-purple-600 hover:bg-purple-700 text-sm">
                  <Plus className="mr-2 h-4 w-4" />
                  Criar Nota Manual
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Adicionar Nota Manual</DialogTitle>
                  <DialogDescription>
                    Digite uma nota personalizada para enriquecer o conhecimento da IA.
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="title">Título</Label>
                    <Input
                      id="title"
                      value={manualTitle}
                      onChange={(e) => setManualTitle(e.target.value)}
                      placeholder="Ex: Regra de Apostas"
                    />
                  </div>
                  <div>
                    <Label htmlFor="category">Categoria</Label>
                    <Select value={manualCategory} onValueChange={setManualCategory}>
                      <SelectTrigger>
                        <SelectValue placeholder="Selecione a categoria" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="livros">Livros/TCCs</SelectItem>
                        <SelectItem value="estatisticas">Estatísticas</SelectItem>
                        <SelectItem value="calendarios">Calendários</SelectItem>
                        <SelectItem value="apis">APIs</SelectItem>
                        <SelectItem value="manuais">Manuais</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label htmlFor="text">Texto</Label>
                    <Textarea
                      id="text"
                      value={manualText}
                      onChange={(e) => setManualText(e.target.value)}
                      placeholder="Digite o conteúdo da nota..."
                      rows={5}
                    />
                  </div>
                </div>
                <DialogFooter>
                  <Button variant="outline" onClick={() => setManualDialogOpen(false)}>
                    Cancelar
                  </Button>
                  <Button onClick={handleManualSubmit} disabled={!manualTitle.trim() || !manualText.trim() || !manualCategory}>
                    Adicionar
                  </Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </CardContent>
        </Card>
      </div>
    </aside>
  )
}