import { useEffect, useState } from "react";

import { checkHealth } from "@/lib/api";

/** Polls the backend's /health endpoint so the top bar can show a live status badge. */
export function useApiHealth(pollIntervalMs = 30_000) {
  const [isOnline, setIsOnline] = useState<boolean | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function poll() {
      const healthy = await checkHealth();
      if (!cancelled) setIsOnline(healthy);
    }

    poll();
    const interval = setInterval(poll, pollIntervalMs);
    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, [pollIntervalMs]);

  return isOnline;
}
