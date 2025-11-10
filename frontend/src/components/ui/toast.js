import { toast } from 'react-hot-toast';

function reducedMotion() {
  if (typeof window === 'undefined' || typeof window.matchMedia !== 'function') return false;
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

export function toastSuccess(message) {
  toast.dismiss();
  toast.success(message, { duration: reducedMotion() ? 1500 : 2000 });
}

export function toastError(message) {
  toast.dismiss();
  toast.error(message, { duration: reducedMotion() ? 2000 : 3000 });
}

export function toastInfo(message) {
  toast.dismiss();
  toast(message, { duration: reducedMotion() ? 1500 : 2500 });
}
