import { useState, useRef } from 'react'
import axios from 'axios'
import { motion } from 'framer-motion'
import { toastError, toastSuccess } from '../components/ui/toast'
import UploadSuccessLottie from '../components/ui/UploadSuccessLottie'
import LoadingLottie from '../components/ui/LoadingLottie'

export default function UploadPage() {
  const [file, setFile] = useState(null)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [uploadedData, setUploadedData] = useState(null)
  const [isUploading, setIsUploading] = useState(false)
  const [showSuccess, setShowSuccess] = useState(false)
  const [lastError, setLastError] = useState(false)
  const dropRef = useRef(null)

  const onFileChosen = (f) => {
    if (!f) return
    if (f.type !== 'application/pdf') {
      toastError('Invalid or unreadable PDF. Please try a different file.')
      return
    }
    if (f.size > 20 * 1024 * 1024) {
      toastError('File too large (max 20MB).')
      return
    }
    setFile(f)
  }

  const handleFileChange = (e) => onFileChosen(e.target.files?.[0])

  const handleDrop = (e) => {
    e.preventDefault()
    const f = e.dataTransfer.files?.[0]
    onFileChosen(f)
  }

  const handleDragOver = (e) => e.preventDefault()

  const handleUpload = async () => {
    if (!file) {
      toastError('No file selected!')
      return
    }
    const formData = new FormData()
    formData.append('file', file)

    try {
      setIsUploading(true)
      setUploadProgress(0)
      setLastError(false)
      const base = import.meta.env.VITE_API_BASE || 'http://localhost:5000'
      const res = await axios.post(`${base}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (p) => {
          if (!p.total) return
          const percent = Math.round((p.loaded * 100) / p.total)
          setUploadProgress(percent)
        },
      })
      setUploadedData(res.data)
      toastSuccess('PDF uploaded successfully!')
      setShowSuccess(true)
      setTimeout(() => setShowSuccess(false), 1500)
    } catch (err) {
      toastError('Upload failed. Please try again.')
      setLastError(true)
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-indigo-500 to-purple-600 p-6">
      <motion.div
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl shadow-xl p-8 w-full max-w-md text-center text-white"
      >
        <h2 className="text-3xl font-bold mb-4">Upload Real Estate Brochure 📄</h2>

        <div
          ref={dropRef}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          role="button"
          aria-label="PDF upload drop zone"
          className="border-2 border-dashed border-white/50 p-6 rounded-xl bg-white/10 cursor-pointer hover:bg-white/20 transition"
          onClick={() => document.getElementById('pdfUpload').click()}
        >
          <input
            id="pdfUpload"
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            className="hidden"
            aria-label="Choose PDF file"
          />
          <label htmlFor="pdfUpload" className="cursor-pointer">
            {file ? file.name : 'Drag & Drop or Click to Upload PDF'}
          </label>
        </div>

        {isUploading && (
          <div className="w-full bg-white/20 rounded-full h-3 mt-4" aria-label="Upload progress">
            <motion.div
              className="bg-emerald-400 h-3 rounded-full"
              style={{ width: `${uploadProgress}%` }}
              transition={{ ease: 'easeOut', duration: 0.2 }}
            />
            <div className="text-sm mt-1">{uploadProgress}%</div>
          </div>
        )}

        <LoadingLottie visible={isUploading} />

        <button
          onClick={handleUpload}
          disabled={isUploading}
          className="mt-5 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60 text-white py-2 px-6 rounded-lg shadow-md transition"
          aria-disabled={isUploading}
        >
          {isUploading ? `Uploading... ${uploadProgress}%` : 'Upload PDF'}
        </button>

        {lastError && file && !isUploading && (
          <button
            onClick={handleUpload}
            className="mt-3 bg-amber-600 hover:bg-amber-700 text-white py-2 px-6 rounded-lg shadow-md transition"
          >
            Retry
          </button>
        )}

        {uploadedData && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="mt-6 p-4 border border-white/20 rounded-2xl bg-white/10 backdrop-blur"
            aria-live="polite"
          >
            <p><strong>File:</strong> {uploadedData.filename}</p>
            <p><strong>Size:</strong> {uploadedData.size} MB</p>
            <p><strong>Uploaded At:</strong> {uploadedData.uploaded_at}</p>
          </motion.div>
        )}

        <UploadSuccessLottie visible={showSuccess} />
      </motion.div>
    </div>
  )
}
