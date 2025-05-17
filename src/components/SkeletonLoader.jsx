import React from 'react';
import styled, { keyframes } from 'styled-components';

const pulse = keyframes`
  0% {
    background-color: rgba(206, 217, 224, 0.2);
  }
  50% {
    background-color: rgba(206, 217, 224, 0.5);
  }
  100% {
    background-color: rgba(206, 217, 224, 0.2);
  }
`;

const BaseSkeleton = styled.div`
  animation: ${pulse} 1.5s ease-in-out infinite;
  background-color: rgba(206, 217, 224, 0.2);
  border-radius: ${props => props.$radius || '4px'};
  margin-bottom: ${props => props.$mb || '0'};
  height: ${props => props.$height || 'auto'};
  width: ${props => props.$width || '100%'};
`;

const ImageSkeleton = styled(BaseSkeleton)`
  aspect-ratio: ${props => props.$aspectRatio || '16/9'};
  min-height: ${props => props.$minHeight || '200px'};
`;

const TextSkeleton = styled(BaseSkeleton)`
  height: ${props => props.$height || '1rem'};
  margin-bottom: ${props => props.$mb || '0.5rem'};
  width: ${props => props.$width || '100%'};
`;

const TitleSkeleton = styled(TextSkeleton)`
  height: 2rem;
  margin-bottom: 1rem;
  width: 70%;
`;

const CardSkeleton = styled.div`
  padding: 1rem;
  border-radius: 8px;
  background: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  margin-bottom: ${props => props.$mb || '1rem'};
`;

const AvatarSkeleton = styled(BaseSkeleton)`
  height: ${props => props.$size || '40px'};
  width: ${props => props.$size || '40px'};
  border-radius: 50%;
`;

const SkeletonRow = styled.div`
  display: flex;
  align-items: center;
  gap: ${props => props.$gap || '0.5rem'};
  margin-bottom: ${props => props.$mb || '0.5rem'};
`;

const SkeletonLoader = ({ variant = 'text', count = 1, ...props }) => {
  const renderSkeleton = (variant, index) => {
    switch (variant) {
      case 'image':
        return <ImageSkeleton key={index} {...props} />;
      case 'title':
        return <TitleSkeleton key={index} {...props} />;
      case 'avatar':
        return <AvatarSkeleton key={index} {...props} />;
      case 'card':
        return (
          <CardSkeleton key={index} {...props}>
            <ImageSkeleton $minHeight="150px" $mb="1rem" />
            <TitleSkeleton />
            <TextSkeleton $width="90%" />
            <TextSkeleton $width="85%" />
          </CardSkeleton>
        );
      case 'post':
        return (
          <CardSkeleton key={index} {...props}>
            <ImageSkeleton $minHeight="250px" $mb="1.5rem" />
            <TitleSkeleton />
            <TextSkeleton $width="100%" />
            <TextSkeleton $width="100%" />
            <TextSkeleton $width="90%" />
            <TextSkeleton $width="60%" $mb="1rem" />
          </CardSkeleton>
        );
      case 'comment':
        return (
          <CardSkeleton key={index} {...props} $mb="0.75rem">
            <SkeletonRow>
              <AvatarSkeleton $size="32px" />
              <TextSkeleton $width="120px" $height="0.8rem" />
            </SkeletonRow>
            <TextSkeleton $width="95%" $height="0.8rem" />
            <TextSkeleton $width="90%" $height="0.8rem" />
          </CardSkeleton>
        );
      default:
        return <TextSkeleton key={index} {...props} />;
    }
  };

  return (
    <>
      {Array.from({ length: count }).map((_, index) => 
        renderSkeleton(variant, index)
      )}
    </>
  );
};

export default SkeletonLoader; 