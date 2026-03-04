const LABELS = {
  RECEIVED: 'Recebido',
  PROCESSING: 'Processando...',
  DONE: 'Concluído',
  ERROR: 'Erro',
};

export default function ProgressPanel({ status, error }) {
  if (!status) return null;
  const isBusy = status === 'RECEIVED' || status === 'PROCESSING';
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-center gap-3">
        {isBusy && (
          <svg className="h-5 w-5 animate-spin text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
        )}
        <div>
          <p className="font-medium text-slate-800">{LABELS[status] || status}</p>
          {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
        </div>
      </div>
    </div>
  );
}
