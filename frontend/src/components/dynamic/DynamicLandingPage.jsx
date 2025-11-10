import { useEffect, useMemo } from 'react';
import HeroSection from './HeroSection';
import AmenitiesSection from './AmenitiesSection';
import ConnectivitySection from './ConnectivitySection';
import FloorPlanSection from './FloorPlanSection';
import FAQsSection from './FAQsSection';
import ErrorBoundary from '../ui/ErrorBoundary';
import { toastInfo, toastError } from '../ui/toast';

export default function DynamicLandingPage({ data }) {
  const overview = data?.project_overview || data?.overview || null;
  const amenities = data?.amenities || [];
  const connectivity = data?.connectivity || [];
  const floorPlans = data?.floor_plans || [];
  const faqs = data?.faqs || [];

  const isPartial = useMemo(() => {
    return !overview || amenities.length === 0 || floorPlans.length === 0 || (Array.isArray(connectivity) ? connectivity.length === 0 : Object.keys(connectivity || {}).length === 0);
  }, [overview, amenities, floorPlans, connectivity]);

  const isLikelyLlmFailure = useMemo(() => {
    const connEmpty = Array.isArray(connectivity) ? connectivity.length === 0 : Object.keys(connectivity || {}).length === 0;
    return !overview && amenities.length === 0 && floorPlans.length === 0 && connEmpty && faqs.length === 0;
  }, [overview, amenities, floorPlans, connectivity, faqs]);

  useEffect(() => {
    if (isPartial) {
      toastInfo('Some text could not be extracted — partial data shown.');
    }
  }, [isPartial]);

  useEffect(() => {
    if (isLikelyLlmFailure) {
      toastError('AI data extraction failed. Please retry later.');
    }
  }, [isLikelyLlmFailure]);

  return (
    <ErrorBoundary>
      <main className="min-h-screen">
        <HeroSection overview={overview} onKnowMoreId="amenities" />
        <AmenitiesSection amenities={amenities} />
        <ConnectivitySection connectivity={connectivity} />
        <FloorPlanSection floor_plans={floorPlans} />
        <FAQsSection faqs={faqs} />
      </main>
    </ErrorBoundary>
  );
}
