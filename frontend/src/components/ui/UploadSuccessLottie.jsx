import Lottie from 'lottie-react';
import successAnim from '/lottie/upload_success.json';

export default function UploadSuccessLottie({ visible }) {
  if (!visible) return null;
  return (
    <div className="mt-4 rounded-2xl backdrop-blur-lg bg-white/15 border border-white/20 p-4">
      <Lottie animationData={successAnim} loop={false} autoplay style={{ height: 120 }} />
    </div>
  );
}
