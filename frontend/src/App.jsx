import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import UploadPage from './pages/UploadPage'
import { Toaster } from 'react-hot-toast'
import PageShell from './components/ui/PageShell'
import Navbar from './components/Navbar'
import ErrorBoundary from './components/ui/ErrorBoundary'

export default function App() {
  return (
    <Router>
      <ErrorBoundary>
        <PageShell>
          <Navbar />
          <Routes>
            <Route path="/" element={<UploadPage />} />
          </Routes>
        </PageShell>
        <Toaster position="top-right" />
      </ErrorBoundary>
    </Router>
  )
}
