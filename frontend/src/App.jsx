import { useState, useEffect, useRef } from 'react';
import { uploadFile, getStatus, getResult } from './lib/api';
import UploadBox from './components/UploadBox';
import ProgressPanel from './components/ProgressPanel';
import ResultPanel from './components/ResultPanel';

const POLL_INTERVAL_MS = 1500;

export default function App() {
  const [requestId, setRequestId] = useState(null);
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const pollRef = useRef(null);

  const stopPolling = () => {
    if (pollRef.current) {
      clearInterval(pollRef.current);
      pollRef.current = null;
    }
  };

  useEffect(() => {
    if (!requestId || status === 'DONE' || status === 'ERROR') {
      stopPolling();
      return;
    }
    const tick = async () => {
      try {
        const data = await getStatus(requestId);
        setStatus(data.status);
        setError(data.error || null);
        if (data.status === 'DONE') {
          stopPolling();
          const res = await getResult(requestId);
          setResult(res);
        }
      } catch (e) {
        setError(e.message);
        stopPolling();
      }
    };
    tick();
    pollRef.current = setInterval(tick, POLL_INTERVAL_MS);
    return stopPolling;
  }, [requestId, status]);

  const handleProcess = async ({ file, provider }) => {
    setError(null);
    setResult(null);
    setStatus('RECEIVED');
    try {
      const data = await uploadFile(file, provider);
      const id = data.request_id ?? data.id;
      if (!id) throw new Error('Resposta sem request_id');
      setRequestId(id);
    } catch (e) {
      setError(e.message);
      setStatus('ERROR');
      setRequestId(null);
    }
  };

  const isProcessing = status === 'RECEIVED' || status === 'PROCESSING';

  return (
    <div className="min-h-screen bg-slate-50 py-8">
      <div className="mx-auto max-w-2xl px-4">
        <h1 className="mb-8 text-2xl font-bold text-slate-900">Orçamento Automatizado</h1>
        <div className="space-y-6">
          <UploadBox onProcess={handleProcess} disabled={isProcessing} />
          <ProgressPanel status={status} error={error} />
          {result && <ResultPanel result={result} />}
        </div>
      </div>
    </div>
  );
}
