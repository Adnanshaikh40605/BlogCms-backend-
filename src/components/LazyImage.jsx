import { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import SkeletonLoader from './SkeletonLoader';
import { getOptimizedImageUrl } from '../utils/imageUtils';

const ImageContainer = styled.div`
  position: relative;
  width: 100%;
  height: ${props => props.$height || 'auto'};
  overflow: hidden;
  background-color: #f0f0f0;
  border-radius: ${props => props.$borderRadius || '0'};
  aspect-ratio: ${props => props.$aspectRatio};
`;

const StyledImage = styled.img`
  width: 100%;
  height: 100%;
  object-fit: ${props => props.$objectFit || 'cover'};
  object-position: ${props => props.$objectPosition || 'center'};
  opacity: ${props => (props.$loaded ? 1 : 0)};
  transition: opacity 0.3s ease-in-out;
  border-radius: ${props => props.$borderRadius || '0'};
`;

const Placeholder = styled(SkeletonLoader)`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
`;

const LazyImage = ({
  src,
  alt,
  height,
  width,
  className,
  borderRadius,
  objectFit = 'cover',
  objectPosition = 'center',
  aspectRatio = '16/9',
  loadingHeight,
  ...props
}) => {
  const [loaded, setLoaded] = useState(false);
  const [error, setError] = useState(false);
  const [isInView, setIsInView] = useState(false);
  const imgRef = useRef(null);
  const containerRef = useRef(null);

  // Set up intersection observer for lazy loading
  useEffect(() => {
    if (!containerRef.current) return;
    
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            setIsInView(true);
            observer.disconnect();
          }
        });
      },
      { 
        rootMargin: '200px', // Load images 200px before they come into view
        threshold: 0.01 
      }
    );
    
    observer.observe(containerRef.current);
    
    return () => {
      if (containerRef.current) {
        observer.disconnect();
      }
    };
  }, [containerRef]);

  // Handle image loading
  useEffect(() => {
    if (!isInView || !src) return;

    const loadImage = async () => {
      try {
        // Try to get optimized image source (WebP if possible) using our utility function
        const optimizedSrc = await getOptimizedImageUrl(src);
        
        // Create a new image object
        const img = new Image();
        img.src = optimizedSrc || src;
        
        img.onload = () => {
          if (imgRef.current) {
            imgRef.current.src = optimizedSrc || src;
          }
          setLoaded(true);
        };
        
        img.onerror = () => {
          console.error(`Failed to load image: ${optimizedSrc || src}`);
          setError(true);
          // Fallback to original src if optimized version fails
          if (optimizedSrc !== src) {
            if (imgRef.current) {
              imgRef.current.src = src;
              setLoaded(true);
              setError(false);
            }
          }
        };
      } catch (err) {
        console.error('Error loading image:', err);
        setError(true);
      }
    };
    
    loadImage();
  }, [src, isInView]);

  return (
    <ImageContainer
      ref={containerRef}
      $height={height}
      $width={width}
      $aspectRatio={aspectRatio}
      $borderRadius={borderRadius}
      className={className}
    >
      {!loaded && !error && (
        <Placeholder 
          variant="image" 
          $height={loadingHeight || '100%'}
          $minHeight={height}
        />
      )}
      
      {isInView && (
        <StyledImage
          ref={imgRef}
          alt={alt}
          $loaded={loaded}
          $objectFit={objectFit}
          $objectPosition={objectPosition}
          $borderRadius={borderRadius}
          loading="lazy"
          {...props}
        />
      )}
      
      {error && <div>Failed to load image</div>}
    </ImageContainer>
  );
};

export default LazyImage; 