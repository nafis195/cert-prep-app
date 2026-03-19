import { useState, useEffect } from 'react'
import VendorList from './components/VendorList'
import CertificationList from './components/CertificationList'
import CertificationDetail from './components/CertificationDetail'
import './App.css'

function App() {
  const [currentView, setCurrentView] = useState('vendors') // 'vendors', 'certifications', 'detail'
  const [selectedVendor, setSelectedVendor] = useState(null)
  const [selectedCertification, setSelectedCertification] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedVendorFilter, setSelectedVendorFilter] = useState('all')

  const handleVendorSelect = (vendor) => {
    setSelectedVendor(vendor)
    setCurrentView('certifications')
  }

  const handleCertificationSelect = (certification) => {
    setSelectedCertification(certification)
    setCurrentView('detail')
  }

  const handleBack = () => {
    if (currentView === 'detail') {
      setCurrentView('certifications')
      setSelectedCertification(null)
    } else if (currentView === 'certifications') {
      setCurrentView('vendors')
      setSelectedVendor(null)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Technical Certification Preparation Application</h1>
      </header>

      <div className="app-content">
        <aside className="sidebar">
          <div className="sidebar-section">
            <h3>Vendor Filter</h3>
            <div className="vendor-filter">
              {['all', 'AWS', 'Azure', 'Cisco', 'Oracle', 'GCP'].map(vendor => (
                <button
                  key={vendor}
                  className={`vendor-btn ${selectedVendorFilter === vendor ? 'active' : ''}`}
                  onClick={() => setSelectedVendorFilter(vendor)}
                >
                  {vendor === 'all' ? 'All Vendors' : vendor}
                </button>
              ))}
            </div>
          </div>

          <div className="sidebar-section">
            <h3>Search</h3>
            <input
              type="text"
              placeholder="Search by title or exam code..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
          </div>
        </aside>

        <main className="main-content">
          {currentView !== 'vendors' && (
            <button className="back-btn" onClick={handleBack}>
              ← Back
            </button>
          )}

          {currentView === 'vendors' && (
            <VendorList
              onVendorSelect={handleVendorSelect}
              searchTerm={searchTerm}
              vendorFilter={selectedVendorFilter}
            />
          )}

          {currentView === 'certifications' && selectedVendor && (
            <CertificationList
              vendor={selectedVendor}
              onCertificationSelect={handleCertificationSelect}
              searchTerm={searchTerm}
            />
          )}

          {currentView === 'detail' && selectedCertification && (
            <CertificationDetail certification={selectedCertification} />
          )}
        </main>
      </div>
    </div>
  )
}

export default App