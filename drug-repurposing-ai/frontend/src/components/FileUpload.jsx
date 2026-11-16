import React, { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

export default function FileUpload() {
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  const onDrop = useCallback(async (acceptedFiles, rejectedFiles) => {
    if (rejectedFiles.length > 0) {
      setError('Invalid file type. Please upload PDF, JPG, JPEG, PNG, or TXT files.')
      return
    }
    if (acceptedFiles.length === 0) return

    const file = acceptedFiles[0]
    const formData = new FormData()
    formData.append('file', file)

    setUploading(true)
    setProgress(0)
    setError(null)

    try {
      const response = await api.post('/upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (event) => {
          const percent = Math.round((event.loaded * 100) / event.total)
          setProgress(percent)
        },
      })
      const { report_id } = response.data
      navigate(`/analysis/${report_id}`)
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.')
    } finally {
      setUploading(false)
    }
  }, [navigate])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
      'text/plain': ['.txt'],
    },
    maxFiles: 1,
    maxSize: 20 * 1024 * 1024,
  })

  return (
    <div className="max-w-xl mx-auto w-full">
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'active' : ''}`}
      >
        <input {...getInputProps()} />
        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📄</div>
        {isDragActive ? (
          <p className="text-primary font-medium">Drop the medical report here...</p>
        ) : (
          <>
            <p className="text-gray-700 font-medium mb-2">Upload Medical Report</p>
            <p className="text-sm text-gray-500">Drag & drop or click to select a file</p>
            <p className="text-xs text-gray-400 mt-2">
              Supported: PDF, JPG, JPEG, PNG, TXT (max 20MB)
            </p>
          </>
        )}
      </div>

      {uploading && (
        <div className="mt-4">
          <div className="flex items-center gap-2 mb-2">
            <span>📎</span>
            <span className="text-sm text-gray-600">Uploading... {progress}%</span>
          </div>
          <div className="progress-bar">
            <div className="progress-bar-fill" style={{ width: `${progress}%` }} />
          </div>
        </div>
      )}

      {error && (
        <div className="mt-4 flex items-center gap-2 p-3 rounded-lg bg-red-50" style={{ color: '#dc2626' }}>
          <span>⚠️</span>
          <p className="text-sm">{error}</p>
        </div>
      )}
    </div>
  )
}
