Next.js 15 frontend scaffold

Instruções rápidas:

- Instalar dependências:

```powershell
cd frontend_next
npm install
```

- Desenvolver (hot-reload):
```powershell
npm run dev
```

- Build produção (gera `out/` estático):
```powershell
npm run build
```

Integração com backend:
- O backend FastAPI pode servir os arquivos estáticos gerados em `out/` (use `next export`). Alternativamente mantenha `next start`/reverse-proxy para SSR.

Notas:
- Este scaffold inclui Tailwind 4, Framer Motion, Radix UI e TypeScript 5.4. Ajuste dependências conforme necessário.
