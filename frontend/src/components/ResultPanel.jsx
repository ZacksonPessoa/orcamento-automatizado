import { useState } from 'react';

function formatPrice(v) {
  if (v == null) return '—';
  const n = typeof v === 'string' ? parseFloat(v) : v;
  return Number.isNaN(n) ? '—' : `R$ ${n.toFixed(2).replace('.', ',')}`;
}

export default function ResultPanel({ result }) {
  const [copiedType, setCopiedType] = useState(null); // 'text' | 'json'
  if (!result?.quote) return null;

  const { quote } = result;
  const items = quote.items || [];
  const total = quote.total ?? 0;
  const currency = quote.currency || 'BRL';

  const textToCopy = () => {
    const lines = items.map((i) => {
      const preco = i.preco_venda != null ? formatPrice(i.preco_venda) : '—';
      return `${i.name || '—'} | Qtd: ${i.qty ?? 1} | Preço: ${preco} | Match: ${i.match_descr || '—'}`;
    });
    lines.push('---');
    lines.push(`Total: ${formatPrice(total)} (${currency})`);
    return lines.join('\n');
  };

  const jsonToCopy = () => JSON.stringify({ extracted: result.extracted, quote: result.quote }, null, 2);

  const copy = (content, type) => {
    navigator.clipboard.writeText(content).then(() => {
      setCopiedType(type);
      setTimeout(() => setCopiedType(null), 2000);
    });
  };

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-lg font-semibold text-slate-800">Resultado</h2>
      {items.length === 0 ? (
        <p className="text-slate-600">Nenhum item extraído.</p>
      ) : (
        <>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-slate-600">
                  <th className="pb-2 pr-4">Item</th>
                  <th className="pb-2 pr-4">Qtd</th>
                  <th className="pb-2 pr-4">Preço</th>
                  <th className="pb-2">Match (FC03000)</th>
                </tr>
              </thead>
              <tbody>
                {items.map((row, i) => (
                  <tr key={i} className="border-b border-slate-100">
                    <td className="py-2 pr-4 font-medium text-slate-800">{row.name || '—'}</td>
                    <td className="py-2 pr-4 text-slate-700">{row.qty ?? 1}</td>
                    <td className="py-2 pr-4">{formatPrice(row.preco_venda)}</td>
                    <td className="py-2 text-slate-600">{row.match_descr || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="mt-4 flex items-center justify-between border-t border-slate-200 pt-4">
            <p className="font-semibold text-slate-800">
              Total: {formatPrice(total)} ({currency})
            </p>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => copy(textToCopy(), 'text')}
                className="rounded bg-slate-100 px-3 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-200"
              >
                {copiedType === 'text' ? 'Copiado!' : 'Copiar texto'}
              </button>
              <button
                type="button"
                onClick={() => copy(jsonToCopy(), 'json')}
                className="rounded bg-slate-100 px-3 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-200"
              >
                {copiedType === 'json' ? 'Copiado!' : 'Copiar JSON'}
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
