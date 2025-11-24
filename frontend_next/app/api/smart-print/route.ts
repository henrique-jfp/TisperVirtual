import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

/**
 * Define a estrutura de dados esperada do script Python.
 * Isso ajuda com o autocompletar e a segurança de tipos.
 */
interface SmartPrintResult {
  content_type: string;
  title?: string;
  teams?: string[];
  players?: string[];
  date?: string;
  data?: Record<string, any>;
  confidence?: number;
  source_url: string;
  extracted_at: string;
  error?: string;
  details?: string;
}

/**
 * Lida com requisições POST para /api/smart-print.
 * Executa o script Python smart_web_printer.py e retorna o resultado.
 */
export async function POST(request: NextRequest): Promise<NextResponse<SmartPrintResult | { error: string; details?: string }>> {
  try {
    // 1. Extrai e valida a URL do corpo da requisição
    const body = await request.json();
    const { url } = body;

    if (!url || typeof url !== 'string') {
      return NextResponse.json({ error: 'A URL é obrigatória e deve ser uma string.' }, { status: 400 });
    }

    // Validação simples do formato da URL
    try {
      new URL(url);
    } catch (_) {
      return NextResponse.json({ error: 'Formato de URL inválido.' }, { status: 400 });
    }

    // 2. Define o caminho para o script e os argumentos
    // O script está em C:\TradeComigo\tools, então subimos um nível a partir de C:\TradeComigo\frontend_next
    const scriptPath = path.resolve(process.cwd(), '..', 'tools', 'smart_web_printer.py');
    const scriptArgs = ['process', url]; // Comando "process" + URL

    // Caminho direto para o executável Python dentro do seu ambiente virtual
    // Isso evita problemas com o PATH do sistema e o atalho da Microsoft Store.
    const pythonExecutable = path.resolve(process.cwd(), '..', '.venv', 'Scripts', 'python.exe');

    // 3. Executa o script Python em um processo filho
    // Usamos uma Promise para aguardar a conclusão do script de forma assíncrona.
    const resultJson = await new Promise<string>((resolve, reject) => {
      // Usamos o caminho absoluto para o executável Python
      const pythonProcess = spawn(pythonExecutable, [scriptPath, ...scriptArgs]);

      let stdout = '';
      let stderr = '';

      // Captura a saída padrão (onde o JSON final será impresso)
      pythonProcess.stdout.on('data', (data: Buffer) => {
        stdout += data.toString('utf-8');
      });

      // Captura a saída de erro (para logs de progresso e erros reais)
      pythonProcess.stderr.on('data', (data: Buffer) => {
        stderr += data.toString('utf-8');
        // Logamos o progresso no console do servidor Next.js para depuração
        console.log(`[Python Log]: ${data.toString('utf-8').trim()}`);
      });

      // Lida com o fechamento do processo
      pythonProcess.on('close', (code: number) => {
        if (code === 0) {
          // Sucesso: resolve a Promise com a saída JSON
          resolve(stdout.trim());
        } else {
          // Erro: rejeita a Promise com os detalhes do erro
          reject(new Error(`Script Python falhou com código ${code}.\n${stderr}`));
        }
      });

      // Lida com erros ao iniciar o processo
      pythonProcess.on('error', (err: Error) => {
        reject(new Error(`Falha ao iniciar o processo Python: ${err.message}`));
      });
    });

    // 4. Analisa a string JSON e a retorna como resposta
    try {
      const result: SmartPrintResult = JSON.parse(resultJson);
      return NextResponse.json(result, { status: 200 });
    } catch (e) {
      console.error('Erro ao analisar JSON do Python:', e);
      console.error('Saída recebida:', resultJson);
      return NextResponse.json({ error: 'A resposta do script não era um JSON válido.' }, { status: 500 });
    }

  } catch (error) { // Tratamento de erro mais seguro
    console.error('[API Smart-Print Error]:', error);
    // Verificação de tipo para o erro capturado
    const details = error instanceof Error ? error.message : String(error);
    return NextResponse.json(
      { error: 'Erro interno do servidor.', details },
      { status: 500 }
    );
  }
}
