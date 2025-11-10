"""
Image Service

Handles image processing, optimization, and metadata extraction
for the interactive gallery feature.
"""
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from PIL import Image, ImageOps
import io
import json
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageService:
    """Service for handling image processing and optimization."""
    
    # Supported image formats and their MIME types
    SUPPORTED_FORMATS = {
        'webp': 'image/webp',
        'jpeg': 'image/jpeg',
        'png': 'image/png'
    }
    
    # Default quality settings for different formats
    DEFAULT_QUALITY = {
        'webp': 80,
        'jpeg': 85,
        'png': 90
    }
    
    def __init__(self, upload_dir: str, static_dir: str):
        """Initialize the image service with directory paths.
        
        Args:
            upload_dir: Directory where uploaded files are stored
            static_dir: Directory for serving static files
        """
        self.upload_dir = Path(upload_dir)
        self.static_dir = Path(static_dir)
        self.ensure_directories()
    
    def ensure_directories(self) -> None:
        """Ensure required directories exist."""
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.static_dir.mkdir(parents=True, exist_ok=True)
        (self.static_dir / 'images').mkdir(exist_ok=True)
        (self.static_dir / 'thumbs').mkdir(exist_ok=True)
    
    def process_uploaded_image(
        self,
        file_data: bytes,
        filename: str,
        upload_id: str,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Process an uploaded image file.
        
        Args:
            file_data: Binary image data
            filename: Original filename
            upload_id: Unique identifier for the upload
            metadata: Optional metadata to include
            
        Returns:
            Dict containing processing results and metadata
        """
        try:
            # Create upload directory if it doesn't exist
            upload_path = self.upload_dir / upload_id
            upload_path.mkdir(exist_ok=True)
            
            # Save original file
            original_path = upload_path / filename
            with open(original_path, 'wb') as f:
                f.write(file_data)
            
            # Process image
            image = Image.open(io.BytesIO(file_data))
            
            # Generate metadata
            image_metadata = {
                'original_filename': filename,
                'upload_id': upload_id,
                'width': image.width,
                'height': image.height,
                'format': image.format.lower() if image.format else 'unknown',
                'size': len(file_data),
                'created_at': datetime.utcnow().isoformat(),
                'metadata': metadata or {}
            }
            
            # Save metadata
            metadata_path = upload_path / f"{filename}.meta.json"
            with open(metadata_path, 'w') as f:
                json.dump(image_metadata, f, indent=2)
            
            # Generate optimized versions
            optimized = self._generate_optimized_versions(
                image=image,
                upload_id=upload_id,
                filename=filename
            )
            
            return {
                'success': True,
                'upload_id': upload_id,
                'original': str(original_path.relative_to(self.upload_dir)),
                'optimized': optimized,
                'metadata': image_metadata
            }
            
        except Exception as e:
            logger.error(f"Error processing image {filename}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'filename': filename,
                'upload_id': upload_id
            }
    
    def _generate_optimized_versions(
        self,
        image: Image.Image,
        upload_id: str,
        filename: str
    ) -> Dict:
        """Generate optimized versions of the image.
        
        Args:
            image: PIL Image object
            upload_id: Upload identifier
            filename: Original filename
            
        Returns:
            Dict with paths to optimized versions
        """
        base_name = Path(filename).stem
        results = {}
        
        # Generate WebP version (primary format)
        webp_path = self.static_dir / 'images' / f"{upload_id}_{base_name}.webp"
        self._save_image(
            image=image,
            path=webp_path,
            format='webp',
            quality=self.DEFAULT_QUALITY['webp']
        )
        results['webp'] = str(webp_path.relative_to(self.static_dir))
        
        # Generate JPEG fallback
        jpeg_path = self.static_dir / 'images' / f"{upload_id}_{base_name}.jpg"
        self._save_image(
            image=image,
            path=jpeg_path,
            format='jpeg',
            quality=self.DEFAULT_QUALITY['jpeg']
        )
        results['jpeg'] = str(jpeg_path.relative_to(self.static_dir))
        
        # Generate thumbnail
        thumbnail_path = self.static_dir / 'thumbs' / f"{upload_id}_{base_name}_thumb.jpg"
        self._generate_thumbnail(
            image=image,
            path=thumbnail_path,
            size=(300, 200)
        )
        results['thumbnail'] = str(thumbnail_path.relative_to(self.static_dir))
        
        return results
    
    def _save_image(
        self,
        image: Image.Image,
        path: Path,
        format: str,
        quality: int = 80,
        **kwargs
    ) -> None:
        """Save image in the specified format."""
        # Ensure the directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to RGB if saving as JPEG
        if format.lower() == 'jpeg' and image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save the image
        image.save(
            path,
            format=format.upper(),
            quality=quality,
            **kwargs
        )
    
    def _generate_thumbnail(
        self,
        image: Image.Image,
        path: Path,
        size: Tuple[int, int],
        quality: int = 75
    ) -> None:
        """Generate a thumbnail for the image."""
        # Create thumbnail
        thumbnail = ImageOps.fit(
            image,
            size,
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.5)
        )
        
        # Save as JPEG for thumbnails
        self._save_image(
            image=thumbnail,
            path=path,
            format='jpeg',
            quality=quality
        )
    
    def get_image_metadata(self, upload_id: str, image_id: str) -> Dict:
        """Get metadata for a specific image."""
        metadata_path = self.upload_dir / upload_id / f"{image_id}.meta.json"
        if not metadata_path.exists():
            return {
                'success': False,
                'error': 'Image not found',
                'upload_id': upload_id,
                'image_id': image_id
            }
        
        try:
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            return {
                'success': True,
                'metadata': metadata
            }
            
        except Exception as e:
            logger.error(f"Error reading metadata for {upload_id}/{image_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'upload_id': upload_id,
                'image_id': image_id
            }
    
    def list_upload_images(self, upload_id: str) -> Dict:
        """List all images for a specific upload."""
        upload_path = self.upload_dir / upload_id
        if not upload_path.exists():
            return {
                'success': False,
                'error': 'Upload not found',
                'upload_id': upload_id
            }
        
        images = []
        
        # Find all metadata files
        for meta_file in upload_path.glob('*.meta.json'):
            try:
                with open(meta_file, 'r') as f:
                    metadata = json.load(f)
                    images.append(metadata)
            except Exception as e:
                logger.error(f"Error reading metadata file {meta_file}: {str(e)}")
        
        return {
            'success': True,
            'upload_id': upload_id,
            'count': len(images),
            'images': images
        }
