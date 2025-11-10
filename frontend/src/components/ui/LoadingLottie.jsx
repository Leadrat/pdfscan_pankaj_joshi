import Lottie from 'lottie-react';
import loadingAnim from '/lottie/loading.json';

export default function LoadingLottie({ visible }) {
  if (!visible) return null;
  return (
    <div className="mt-4 rounded-2xl backdrop-blur-lg bg-white/15 border border-white/20 p-4 flex items-center justify-center">
      <Lottie animationData={loadingAnim} loop autoplay style={{ height: 80 }} />
    </div>
  );
}
