export function normalizeConnectivity(raw) {
  if (!raw) return [];
  // Accept either {schools:[], hospitals:[], transport:[]} or ["Name - Distance", ...]
  const out = [];
  const pushParsed = (type, item) => {
    if (!item) return;
    const [label, distance = ""] = String(item).split(/\s*-\s*/);
    out.push({ type, label: label?.trim() || "", distance: distance?.trim() || "" });
  };
  if (Array.isArray(raw)) {
    raw.forEach((s) => pushParsed("Place", s));
    return out;
  }
  if (typeof raw === "object") {
    Object.entries(raw).forEach(([k, arr]) => {
      if (Array.isArray(arr)) arr.forEach((s) => pushParsed(k.replace(/s$/i, ''), s));
    });
    return out;
  }
  return out;
}
