"""
Image Gallery API Routes

Handles all image gallery related API endpoints.
"""
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import json

# Import the image service
from ..services.image_service import ImageService

# Create blueprint
image_bp = Blueprint('image_api', __name__, url_prefix='/api/images')

def get_image_service() -> ImageService:
    """Get an instance of the ImageService with app config."""
    return ImageService(
        upload_dir=current_app.config.get('UPLOAD_FOLDER', 'uploads'),
        static_dir=current_app.config.get('STATIC_FOLDER', 'static')
    )

@image_bp.route('/<upload_id>', methods=['GET'])
def get_upload_images(upload_id: str):
    """
    Get all images for a specific upload
    ---
    tags:
      - Gallery
    parameters:
      - name: upload_id
        in: path
        required: true
        description: ID of the upload to get images for
        schema:
          type: string
    responses:
      200:
        description: List of images for the upload
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/GalleryResponse'
      404:
        description: Upload not found
    """
    image_service = get_image_service()
    result = image_service.list_upload_images(upload_id)
    
    if not result['success']:
        return jsonify({
            'success': False,
            'error': result.get('error', 'Unknown error')
        }), 404
    
    return jsonify({
        'success': True,
        'data': {
            'upload_id': upload_id,
            'images': result['images'],
            'count': result['count']
        }
    })

@image_bp.route('/<upload_id>/<image_id>/metadata', methods=['GET'])
def get_image_metadata(upload_id: str, image_id: str):
    """
    Get metadata for a specific image
    ---
    tags:
      - Gallery
    parameters:
      - name: upload_id
        in: path
        required: true
        description: ID of the upload
        schema:
          type: string
      - name: image_id
        in: path
        required: true
        description: ID of the image
        schema:
          type: string
    responses:
      200:
        description: Image metadata
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ImageMetadataResponse'
      404:
        description: Image not found
    """
    image_service = get_image_service()
    result = image_service.get_image_metadata(upload_id, image_id)
    
    if not result['success']:
        return jsonify({
            'success': False,
            'error': result.get('error', 'Image not found')
        }), 404
    
    return jsonify({
        'success': True,
        'data': {
            'upload_id': upload_id,
            'image_id': image_id,
            'metadata': result['metadata']
        }
    })

@image_bp.route('/<upload_id>/<image_id>/download', methods=['GET'])
def download_image(upload_id: str, image_id: str):
    """
    Download an image file
    ---
    tags:
      - Gallery
    parameters:
      - name: upload_id
        in: path
        required: true
        description: ID of the upload
        schema:
          type: string
      - name: image_id
        in: path
        required: true
        description: ID of the image
        schema:
          type: string
      - name: format
        in: query
        required: false
        description: Preferred image format (webp, jpeg, png)
        schema:
          type: string
          enum: [webp, jpeg, png]
          default: webp
    responses:
      200:
        description: Image file
        content:
          image/*:
            schema:
              type: string
              format: binary
      404:
        description: Image not found
    """
    image_service = get_image_service()
    image_format = request.args.get('format', 'webp').lower()
    
    # Get image metadata to find the file
    result = image_service.get_image_metadata(upload_id, image_id)
    if not result['success']:
        return jsonify({
            'success': False,
            'error': result.get('error', 'Image not found')
        }), 404
    
    # Determine the file path based on requested format
    metadata = result['metadata']
    file_path = None
    mime_type = None
    
    if image_format == 'webp' and 'optimized' in metadata and 'webp' in metadata['optimized']:
        file_path = Path(current_app.config.get('STATIC_FOLDER', 'static')) / metadata['optimized']['webp']
        mime_type = 'image/webp'
    elif image_format == 'jpeg' and 'optimized' in metadata and 'jpeg' in metadata['optimized']:
        file_path = Path(current_app.config.get('STATIC_FOLDER', 'static')) / metadata['optimized']['jpeg']
        mime_type = 'image/jpeg'
    elif image_format == 'png' and 'optimized' in metadata and 'png' in metadata['optimized']:
        file_path = Path(current_app.config.get('STATIC_FOLDER', 'static')) / metadata['optimized']['png']
        mime_type = 'image/png'
    else:
        # Fallback to original file if specific format not found
        file_path = Path(current_app.config.get('UPLOAD_FOLDER', 'uploads')) / upload_id / metadata['original_filename']
        mime_type = f"image/{metadata.get('format', 'jpeg')}"
    
    if not file_path or not file_path.exists():
        return jsonify({
            'success': False,
            'error': 'File not found'
        }), 404
    
    # Send the file
    return send_from_directory(
        directory=file_path.parent,
        path=file_path.name,
        mimetype=mime_type,
        as_attachment=False,
        download_name=f"{upload_id}_{image_id}.{image_format}"
    )

@image_bp.route('/upload', methods=['POST'])
def upload_image():
    """
    Upload a new image
    ---
    tags:
      - Gallery
    requestBody:
      required: true
      content:
        multipart/form-data:
          schema:
            type: object
            properties:
              file:
                type: string
                format: binary
                description: Image file to upload
              upload_id:
                type: string
                description: ID of the upload (will be created if not provided)
              metadata:
                type: string
                description: Optional JSON metadata
    responses:
      201:
        description: Image uploaded successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UploadResponse'
      400:
        description: Invalid request
    """
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No file part in the request'
        }), 400
    
    file = request.files['file']
    
    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No selected file'
        }), 400
    
    if file:
        # Get or generate upload ID
        upload_id = request.form.get('upload_id')
        if not upload_id:
            upload_id = f"upload_{int(datetime.utcnow().timestamp())}"
        
        # Parse metadata if provided
        metadata = {}
        if 'metadata' in request.form:
            try:
                metadata = json.loads(request.form['metadata'])
            except json.JSONDecodeError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid metadata format. Must be valid JSON.'
                }), 400
        
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Get image service
        image_service = get_image_service()
        
        try:
            # Process the uploaded file
            result = image_service.process_uploaded_image(
                file_data=file.read(),
                filename=filename,
                upload_id=upload_id,
                metadata=metadata
            )
            
            if not result['success']:
                return jsonify({
                    'success': False,
                    'error': result.get('error', 'Failed to process image')
                }), 500
            
            return jsonify({
                'success': True,
                'upload_id': upload_id,
                'image_id': Path(filename).stem,
                'optimized': result['optimized'],
                'metadata': result['metadata']
            }), 201
            
        except Exception as e:
            current_app.logger.error(f"Error processing upload: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to process image',
                'details': str(e)
            }), 500
    
    return jsonify({
        'success': False,
        'error': 'Invalid file'
    }), 400

def init_app(app):
    """Initialize the image routes with the Flask app."""
    # Register the blueprint
    app.register_blueprint(image_bp)
    
    # Ensure upload and static directories exist
    upload_dir = Path(app.config.get('UPLOAD_FOLDER', 'uploads'))
    static_dir = Path(app.config.get('STATIC_FOLDER', 'static'))
    
    upload_dir.mkdir(parents=True, exist_ok=True)
    static_dir.mkdir(parents=True, exist_ok=True)
    (static_dir / 'images').mkdir(exist_ok=True)
    (static_dir / 'thumbs').mkdir(exist_ok=True)
    
    return app
