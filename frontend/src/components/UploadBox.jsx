import { useState } from 'react';

const PROVIDERS = [
  { value: 'auto', label: 'AUTO' },
  { value: 'google', label: 'GOOGLE' },
  { value: 'aws', label: 'AWS' },
  { value: 'tesseract', label: 'TESSERACT' },
];

const ACCEPT = '.jpg,.jpeg,.png,.pdf,.txt';
const MAX_MB = 15;

export default function UploadBox({ onProcess, disabled }) {
  const [file, setFile] = useState(null);
  const [provider, setProvider] = useState('auto');
  const [error, setError] = useState('');

  const handleFile = (e) => {
    setError('');
    const f = e.target.files?.[0];
    if (!f) {
      setFile(null);
      return;
    }
    if (f.size > MAX_MB * 1024 * 1024) {
      setError(`Arquivo deve ter no máximo ${MAX_MB} MB`);
      setFile(null);
      return;
    }
    const ext = (f.name || '').split('.').pop()?.toLowerCase();
    const allowed = ['jpg', 'jpeg', 'png', 'pdf', 'txt'];
    if (!allowed.includes(ext)) {
      setError('Use JPG, PNG, PDF ou TXT');
      setFile(null);
      return;
    }
    setFile(f);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    if (!file) {
      setError('Selecione um arquivo');
      return;
    }
    onProcess({ file, provider });
  };

  return (
    <form onSubmit={handleSubmit} className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-lg font-semibold text-slate-800">Enviar arquivo</h2>
      <div className="mb-4">
        <label className="mb-2 block text-sm font-medium text-slate-600">Arquivo (imagem ou .txt)</label>
        <input
          type="file"
          accept={ACCEPT}
          onChange={handleFile}
          disabled={disabled}
          className="block w-full text-sm text-slate-600 file:mr-4 file:rounded file:border-0 file:bg-slate-100 file:px-4 file:py-2 file:text-slate-700"
        />
        {file && <p className="mt-1 text-sm text-slate-500">{file.name}</p>}
      </div>
      <div className="mb-4">
        <label className="mb-2 block text-sm font-medium text-slate-600">Provider OCR</label>
        <select
          value={provider}
          onChange={(e) => setProvider(e.target.value)}
          disabled={disabled}
          className="w-full rounded border border-slate-300 px-3 py-2 text-slate-700 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        >
          {PROVIDERS.map((p) => (
            <option key={p.value} value={p.value}>{p.label}</option>
          ))}
        </select>
      </div>
      {error && <p className="mb-4 text-sm text-red-600">{error}</p>}
      <button
        type="submit"
        disabled={disabled || !file}
        className="w-full rounded-lg bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
      >
        Processar
      </button>
    </form>
  );
}
