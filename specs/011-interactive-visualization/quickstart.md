# Quickstart Guide: Interactive Visualization & Performance Audit

**Feature**: 011-interactive-visualization  
**Date**: 2025-11-10  
**Target Audience**: Developers implementing the image gallery and viewer

## Overview

This guide provides implementation hints and best practices for building the interactive image viewer with zoom/pan, carousel navigation, and performance optimization. The implementation integrates with the existing Leadrat brochure system.

## Prerequisites

- React 18+ with Vite build system
- TailwindCSS for styling
- Framer Motion for animations
- Existing upload/OCR pipeline
- Glassmorphism theme tokens

## Core Implementation Steps

### 1. Install Dependencies

```bash
# Core zoom/pan library
npm install react-medium-image-zoom

# Already installed from previous specs
# npm install framer-motion
# npm install @tailwindcss/aspect-ratio
```

### 2. Create Gallery Components Structure

```
frontend/src/components/gallery/
├── Gallery.jsx              # Main gallery container
├── GalleryCard.jsx          # Individual image card
├── ImageModal.jsx           # Modal viewer with zoom
├── CarouselControls.jsx     # Next/prev navigation
├── LoadingSkeleton.jsx      # Loading states
└── ErrorBoundary.jsx        # Error handling
```

### 3. Implement Responsive Grid Gallery

```jsx
// Gallery.jsx
import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import GalleryCard from './GalleryCard';
import ImageModal from './ImageModal';
import LoadingSkeleton from './LoadingSkeleton';

const Gallery = ({ images = [], config = {} }) => {
  const [galleryState, setGalleryState] = useState({
    isOpen: false,
    currentIndex: 0,
    loading: true,
    loadingImages: new Set(),
    error: null
  });

  const defaultConfig = {
    columns: { mobile: 1, tablet: 2, desktop: 3 },
    lazyLoad: true,
    preloadCount: 2,
    imageTimeout: 10000,
    maxRetries: 2,
    maxZoom: 3.0,
    enableAnimations: true,
    enableKeyboard: true
  };

  const finalConfig = { ...defaultConfig, ...config };

  const openModal = useCallback((index) => {
    setGalleryState(prev => ({
      ...prev,
      isOpen: true,
      currentIndex: index
    }));
  }, []);

  const closeModal = useCallback(() => {
    setGalleryState(prev => ({ ...prev, isOpen: false }));
  }, []);

  const navigateImage = useCallback((direction) => {
    setGalleryState(prev => {
      const newIndex = direction === 'next' 
        ? (prev.currentIndex + 1) % images.length
        : (prev.currentIndex - 1 + images.length) % images.length;
      return { ...prev, currentIndex: newIndex };
    });
  }, [images.length]);

  return (
    <div className="w-full">
      {/* Gallery Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <AnimatePresence>
          {images.map((image, index) => (
            <motion.div
              key={image.sourceId}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
            >
              <GalleryCard
                image={image}
                onClick={() => openModal(index)}
                config={finalConfig}
              />
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {/* Modal Viewer */}
      <AnimatePresence>
        {galleryState.isOpen && (
          <ImageModal
            images={images}
            currentIndex={galleryState.currentIndex}
            onClose={closeModal}
            onNavigate={navigateImage}
            config={finalConfig}
          />
        )}
      </AnimatePresence>
    </div>
  );
};

export default Gallery;
```

### 4. Implement Gallery Card with Glassmorphism

```jsx
// GalleryCard.jsx
import { forwardRef } from 'react';
import { motion } from 'framer-motion';

const GalleryCard = forwardRef(({ image, onClick, config }, ref) => {
  const handleImageLoad = () => {
    // Performance logging in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`Image loaded: ${image.sourceId}`, {
        fileSize: image.fileSize,
        format: image.format,
        loadTime: performance.now()
      });
    }
  };

  const handleImageError = () => {
    // Retry logic would go here
    console.error(`Failed to load image: ${image.sourceId}`);
  };

  return (
    <motion.div
      ref={ref}
      whileHover={{ scale: 1.02 }}
      whileFocus={{ scale: 1.02 }}
      className="group relative overflow-hidden rounded-xl backdrop-blur-md bg-white/10 border border-white/20 shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer"
      onClick={onClick}
      tabIndex={0}
      role="button"
      aria-label={`View image: ${image.altText}`}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onClick();
        }
      }}
    >
      {/* Image Container */}
      <div className="aspect-w-16 aspect-h-12 relative">
        <picture>
          <source srcSet={image.url} type="image/webp" />
          <source srcSet={image.fallbackUrl} type="image/jpeg" />
          <img
            src={image.fallbackUrl}
            alt={image.altText}
            className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
            onLoad={handleImageLoad}
            onError={handleImageError}
            loading="lazy"
          />
        </picture>
        
        {/* Overlay Gradient */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      </div>

      {/* Caption */}
      <div className="absolute bottom-0 left-0 right-0 p-4">
        <p className="text-white text-sm font-medium line-clamp-2">
          {image.caption}
        </p>
      </div>

      {/* Focus Ring */}
      <div className="absolute inset-0 rounded-xl ring-2 ring-emerald-400/50 ring-offset-2 ring-offset-transparent opacity-0 group-focus:opacity-100 transition-opacity duration-200" />
    </motion.div>
  );
});

GalleryCard.displayName = 'GalleryCard';

export default GalleryCard;
```

### 5. Implement Modal with Zoom and Carousel

```jsx
// ImageModal.jsx
import { useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Zoom from 'react-medium-image-zoom';
import 'react-medium-image-zoom/dist/styles.css';
import CarouselControls from './CarouselControls';

const ImageModal = ({ images, currentIndex, onClose, onNavigate, config }) => {
  const handleKeyDown = useCallback((e) => {
    if (!config.enableKeyboard) return;
    
    switch (e.key) {
      case 'Escape':
        onClose();
        break;
      case 'ArrowLeft':
        onNavigate('prev');
        break;
      case 'ArrowRight':
        onNavigate('next');
        break;
    }
  }, [config.enableKeyboard, onClose, onNavigate]);

  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown);
    document.body.style.overflow = 'hidden';
    
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'unset';
    };
  }, [handleKeyDown]);

  const currentImage = images[currentIndex];

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm"
        onClick={onClose}
        role="dialog"
        aria-modal="true"
        aria-label={`Image gallery, ${currentIndex + 1} of ${images.length}`}
      >
        {/* Modal Content */}
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          transition={{ duration: 0.3 }}
          className="relative max-w-7xl max-h-[90vh] mx-4"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Image Container */}
          <div className="relative bg-gradient-to-br from-indigo-500/20 to-purple-600/20 rounded-2xl p-2 backdrop-blur-md border border-white/20">
            <Zoom
              zoomMargin={20}
              scrollableEl={window}
              zoomImg={{
                src: currentImage.url,
                alt: currentImage.altText,
                className: 'max-w-none max-h-none'
              }}
            >
              <picture>
                <source srcSet={currentImage.url} type="image/webp" />
                <source srcSet={currentImage.fallbackUrl} type="image/jpeg" />
                <img
                  src={currentImage.fallbackUrl}
                  alt={currentImage.altText}
                  className="max-w-full max-h-[80vh] object-contain rounded-xl"
                />
              </picture>
            </Zoom>

            {/* Image Caption */}
            <div className="absolute bottom-4 left-4 right-4 bg-black/60 backdrop-blur-sm rounded-lg p-3">
              <p className="text-white text-sm font-medium">
                {currentImage.caption}
              </p>
              <p className="text-white/70 text-xs mt-1">
                {currentIndex + 1} of {images.length}
              </p>
            </div>
          </div>

          {/* Close Button */}
          <button
            onClick={onClose}
            className="absolute -top-4 -right-4 w-10 h-10 bg-emerald-400 hover:bg-emerald-500 text-black rounded-full flex items-center justify-center transition-colors duration-200 shadow-lg"
            aria-label="Close modal"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

          {/* Carousel Controls */}
          {images.length > 1 && (
            <CarouselControls
              currentIndex={currentIndex}
              totalCount={images.length}
              onNavigate={onNavigate}
              config={config}
            />
          )}
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default ImageModal;
```

### 6. Implement Lazy Loading with Intersection Observer

```jsx
// hooks/useLazyLoad.js
import { useState, useEffect, useRef } from 'react';

export const useLazyLoad = (threshold = 0.1) => {
  const [isIntersecting, setIsIntersecting] = useState(false);
  const [hasLoaded, setHasLoaded] = useState(false);
  const elementRef = useRef(null);

  useEffect(() => {
    const element = elementRef.current;
    if (!element) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !hasLoaded) {
          setIsIntersecting(true);
          setHasLoaded(true);
        }
      },
      { threshold }
    );

    observer.observe(element);

    return () => {
      observer.unobserve(element);
    };
  }, [threshold, hasLoaded]);

  return { elementRef, isIntersecting, hasLoaded };
};
```

### 7. Add Performance Monitoring

```jsx
// utils/performance.js
export const logPerformance = (eventName, data = {}) => {
  if (process.env.NODE_ENV !== 'development') return;

  const timestamp = performance.now();
  console.log(`[Performance] ${eventName}`, {
    timestamp,
    ...data
  });

  // Send to analytics in production if needed
  if (process.env.NODE_ENV === 'production' && window.gtag) {
    window.gtag('event', eventName, {
      custom_parameter_1: data.duration,
      custom_parameter_2: data.imageCount
    });
  }
};

export const measureImageLoad = (imageUrl) => {
  const startTime = performance.now();
  
  return new Promise((resolve, reject) => {
    const img = new Image();
    
    img.onload = () => {
      const duration = performance.now() - startTime;
      logPerformance('image_load', {
        url: imageUrl,
        duration: Math.round(duration)
      });
      resolve({ duration, success: true });
    };
    
    img.onerror = () => {
      const duration = performance.now() - startTime;
      logPerformance('image_load_error', {
        url: imageUrl,
        duration: Math.round(duration)
      });
      reject({ duration, success: false });
    };
    
    img.src = imageUrl;
  });
};
```

## Integration with Existing System

### 1. Connect to Upload Pipeline

```jsx
// pages/DynamicLandingPage.jsx
import { useState, useEffect } from 'react';
import Gallery from '../components/gallery/Gallery';
import { fetchImagesByUploadId } from '../services/galleryService';

const DynamicLandingPage = ({ uploadId }) => {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadImages = async () => {
      try {
        const response = await fetchImagesByUploadId(uploadId);
        setImages(response.data.images);
      } catch (error) {
        console.error('Failed to load images:', error);
      } finally {
        setLoading(false);
      }
    };

    if (uploadId) {
      loadImages();
    }
  }, [uploadId]);

  if (loading) {
    return <GallerySkeleton />;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <section className="mb-12">
        <h2 className="text-3xl font-bold text-white mb-6">
          Property Gallery
        </h2>
        <Gallery 
          images={images}
          config={{
            columns: { mobile: 1, tablet: 2, desktop: 3 },
            enableAnimations: true,
            maxZoom: 3.0
          }}
        />
      </section>
    </div>
  );
};
```

### 2. API Service Integration

```jsx
// services/galleryService.js
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:5000/api';

export const fetchImagesByUploadId = async (uploadId, format = 'webp') => {
  const response = await axios.get(`${API_BASE}/images/${uploadId}`, {
    params: { format }
  });
  return response.data;
};

export const fetchImageMetadata = async (uploadId, imageId) => {
  const response = await axios.get(`${API_BASE}/images/${uploadId}/${imageId}/metadata`);
  return response.data;
};

export const downloadImage = async (uploadId, imageId, format = 'original') => {
  const response = await axios.get(`${API_BASE}/images/${uploadId}/${imageId}/download`, {
    params: { format },
    responseType: 'blob'
  });
  return response.data;
};
```

## Testing Scenarios

### 1. Unit Testing

```jsx
// __tests__/Gallery.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import Gallery from '../components/gallery/Gallery';

const mockImages = [
  {
    sourceId: 'test_001',
    url: '/test/image.webp',
    fallbackUrl: '/test/image.jpg',
    thumbnailUrl: '/test/thumb.jpg',
    caption: 'Test Image',
    altText: 'Test image for gallery',
    width: 1200,
    height: 800,
    aspectRatio: 1.5,
    fileSize: 250000,
    format: 'webp'
  }
];

describe('Gallery', () => {
  test('renders gallery cards', () => {
    render(<Gallery images={mockImages} />);
    expect(screen.getByAltText('Test image for gallery')).toBeInTheDocument();
  });

  test('opens modal on card click', () => {
    render(<Gallery images={mockImages} />);
    const card = screen.getByRole('button');
    fireEvent.click(card);
    expect(screen.getByRole('dialog')).toBeInTheDocument();
  });

  test('supports keyboard navigation', () => {
    render(<Gallery images={mockImages} />);
    const card = screen.getByRole('button');
    fireEvent.keyDown(card, { key: 'Enter' });
    expect(screen.getByRole('dialog')).toBeInTheDocument();
  });
});
```

### 2. Performance Testing

```bash
# Lighthouse CI configuration
npm install -g @lhci/cli

# Run performance audit
lhci autorun --upload.target=temporary-public-storage

# Expected scores:
# Performance: ≥90
# Accessibility: ≥90
# Best Practices: ≥90
# SEO: ≥90
```

### 3. Accessibility Testing

```bash
# Install axe-core for automated accessibility testing
npm install --save-dev @axe-core/react

# Run accessibility audit
npx axe http://localhost:3000 --tags wcag2a,wcag2aa
```

## Performance Optimization Checklist

- [ ] Implement WebP format with fallbacks
- [ ] Add lazy loading with Intersection Observer
- [ ] Use React.memo for expensive components
- [ ] Implement code splitting for gallery components
- [ ] Add image preloading for carousel navigation
- [ ] Optimize bundle size with tree shaking
- [ ] Enable gzip compression on server
- [ ] Set proper cache headers for static assets
- [ ] Implement service worker for offline viewing
- [ ] Monitor Core Web Vitals in production

## Accessibility Checklist

- [ ] All interactive elements have ARIA labels
- [ ] Keyboard navigation works (Tab, Enter, Space, Arrow keys, ESC)
- [ ] Focus indicators are visible
- [ ] Color contrast meets WCAG AA standards
- [ ] Images have descriptive alt text
- [ ] Modal focus trapping implemented
- [ ] Reduced motion preferences respected
- [ ] Screen reader announcements for state changes
- [ ] Semantic HTML structure maintained
- [ ] Touch gestures have keyboard alternatives

## Troubleshooting

### Common Issues

1. **Images not loading**: Check CORS headers and file paths
2. **Zoom not working**: Verify react-medium-image-zoom styles are imported
3. **Performance issues**: Enable React DevTools Profiler to identify bottlenecks
4. **Accessibility failures**: Run axe-core audit for specific violations
5. **Animation jank**: Use will-change CSS property and GPU acceleration

### Debug Tools

- React DevTools for component inspection
- Chrome DevTools Performance tab for animation analysis
- Lighthouse for overall performance audit
- axe DevTools for accessibility testing
- Network tab for image loading optimization

## Next Steps

1. Implement the basic gallery structure
2. Add zoom/pan functionality with react-medium-image-zoom
3. Integrate with existing upload pipeline
4. Implement performance monitoring
5. Run accessibility and performance audits
6. Deploy and monitor Core Web Vitals

This implementation provides a solid foundation for the interactive image viewer while maintaining the glassmorphism theme and performance targets specified in the requirements.
