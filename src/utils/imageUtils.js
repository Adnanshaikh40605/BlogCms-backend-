// Helper functions for working with images

/**
 * Check if WebP format is supported in the current browser
 * @returns {Promise<boolean>} Whether WebP is supported
 */
export const supportsWebP = async () => {
  if (!self.createImageBitmap) return false;
  
  const webpData = 'data:image/webp;base64,UklGRh4AAABXRUJQVlA4TBEAAAAvAAAAAAfQ//73v/+BiOh/AAA=';
  const blob = await fetch(webpData).then(r => r.blob());
  
  return createImageBitmap(blob).then(() => true, () => false);
};

/**
 * Try to get WebP version of an image URL if supported
 * @param {string} originalSrc - Original image URL
 * @returns {Promise<string>} The optimized image URL (WebP if supported)
 */
export const getOptimizedImageUrl = async (originalSrc) => {
  if (!originalSrc) return null;
  
  // If already WebP, use as is
  if (originalSrc.toLowerCase().endsWith('.webp')) {
    return originalSrc;
  }
  
  // Check if WebP is supported
  const webpSupport = await supportsWebP();
  if (!webpSupport) {
    return originalSrc;
  }
  
  // Try to get WebP version by replacing extension
  try {
    const baseSrc = originalSrc.substring(0, originalSrc.lastIndexOf('.'));
    const webpSrc = `${baseSrc}.webp`;
    
    // Check if WebP version exists
    const response = await fetch(webpSrc, { method: 'HEAD' });
    if (response.ok) {
      return webpSrc;
    }
  } catch (err) {
    console.warn('Error checking WebP version:', err);
  }
  
  return originalSrc;
};

/**
 * Create a placeholder color from a string (like post title)
 * Used for generating consistent placeholder colors
 * @param {string} str - String to hash
 * @returns {string} CSS color
 */
export const stringToColor = (str) => {
  if (!str) return '#f0f0f0';
  
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
  }
  
  let color = '#';
  for (let i = 0; i < 3; i++) {
    const value = (hash >> (i * 8)) & 0xFF;
    // Ensure lighter colors by limiting value range (200-240)
    const adjustedValue = 200 + (value % 40);
    color += adjustedValue.toString(16).padStart(2, '0');
  }
  
  return color;
};

/**
 * Generate thumbnail sizes based on screen size
 * @param {string} originalSrc - Original image source
 * @returns {object} Object with different sized thumbnails
 */
export const generateThumbnailSizes = (originalSrc) => {
  if (!originalSrc) return {};
  
  // Extract base path and extension
  const lastDotIndex = originalSrc.lastIndexOf('.');
  if (lastDotIndex === -1) return { original: originalSrc };
  
  const basePath = originalSrc.substring(0, lastDotIndex);
  const extension = originalSrc.substring(lastDotIndex);
  
  return {
    original: originalSrc,
    small: `${basePath}-small${extension}`,    // e.g. 300px width
    medium: `${basePath}-medium${extension}`,  // e.g. 600px width
    large: `${basePath}-large${extension}`,    // e.g. 1200px width
  };
};

/**
 * Generate CSS for responsive image based on thumbnail sizes
 * @param {object} thumbnails - Thumbnail sizes from generateThumbnailSizes
 * @returns {string} CSS for srcSet and sizes
 */
export const getResponsiveImageProps = (thumbnails) => {
  if (!thumbnails || !thumbnails.original) return {};
  
  return {
    srcSet: `
      ${thumbnails.small || thumbnails.original} 300w,
      ${thumbnails.medium || thumbnails.original} 600w,
      ${thumbnails.large || thumbnails.original} 1200w,
      ${thumbnails.original} 2000w
    `,
    sizes: `
      (max-width: 600px) 300px,
      (max-width: 1200px) 600px,
      1200px
    `
  };
}; 