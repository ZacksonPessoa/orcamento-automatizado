import { useState, useRef } from 'react';

const ACCEPT = '.png,.jpg,.jpeg,.webp,.pdf,.txt';
const ALLOWED_EXT = ['png', 'jpg', 'jpeg', 'webp', 'pdf', 'txt'];
const MAX_MB = 15;

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function validateFile(f) {
  if (!f) return null;
  if (f.size > MAX_MB * 1024 * 1024) return `Arquivo deve ter no máximo ${MAX_MB} MB`;
  const ext = (f.name || '').split('.').pop()?.toLowerCase();
  if (!ALLOWED_EXT.includes(ext)) return 'Use PNG, JPG, WEBP, PDF ou TXT';
  return null;
}

export default function UploadBox({ onProcess, disabled }) {
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const inputRef = useRef(null);

  const setFileWithValidation = (f) => {
    setError('');
    if (!f) {
      setFile(null);
      return;
    }
    const err = validateFile(f);
    if (err) {
      setError(err);
      setFile(null);
      return;
    }
    setFile(f);
  };

  const handleFileChange = (e) => {
    setFileWithValidation(e.target.files?.[0] ?? null);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const f = e.dataTransfer?.files?.[0];
    setFileWithValidation(f ?? null);
  };

  const handleZoneClick = () => {
    if (!disabled) inputRef.current?.click();
  };

  const handleRemove = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setFile(null);
    setError('');
    if (inputRef.current) inputRef.current.value = '';
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    if (!file) {
      setError('Selecione um arquivo');
      return;
    }
    onProcess({ file });
  };

  return (
    <form onSubmit={handleSubmit} className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-lg font-semibold text-slate-800">Enviar arquivo</h2>

      <input
        ref={inputRef}
        type="file"
        accept={ACCEPT}
        onChange={handleFileChange}
        className="hidden"
        disabled={disabled}
      />

      <div
        role="button"
        tabIndex={0}
        onClick={handleZoneClick}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onKeyDown={(e) => e.key === 'Enter' && handleZoneClick()}
        className={`mb-4 cursor-pointer rounded-xl border-2 border-dashed px-6 py-8 text-center transition-colors ${
          isDragging
            ? 'border-blue-400 bg-blue-50'
            : 'border-slate-200 bg-slate-50 hover:border-slate-300 hover:bg-slate-100'
        } ${disabled ? 'pointer-events-none opacity-60' : ''}`}
      >
        <p className="text-slate-600">
          Arraste e solte ou clique para selecionar
        </p>
        <p className="mt-1 text-sm text-slate-500">
          PNG, JPG, WEBP, PDF ou TXT (máx. {MAX_MB} MB)
        </p>
      </div>

      {file && (
        <div className="mb-4 flex items-center justify-between rounded-lg border border-slate-200 bg-slate-50 px-4 py-3">
          <div className="min-w-0">
            <p className="truncate text-sm font-medium text-slate-800">{file.name}</p>
            <p className="text-xs text-slate-500">{formatSize(file.size)}</p>
          </div>
          <button
            type="button"
            onClick={handleRemove}
            disabled={disabled}
            className="shrink-0 rounded px-3 py-1.5 text-sm font-medium text-slate-600 hover:bg-slate-200 disabled:opacity-50"
          >
            Remover
          </button>
        </div>
      )}

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
