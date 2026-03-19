import React, { useState, useEffect } from 'react';

function VendorList({ onVendorSelect, searchTerm, vendorFilter }) {
  const [vendors, setVendors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/vendors')
      .then(response => response.json())
      .then(data => {
        setVendors(data);
        setLoading(false);
      })
      .catch(error => {
        setError(error.message);
        setLoading(false);
      });
  }, []);

  const filteredVendors = vendors.filter(vendor => {
    const matchesSearch = vendor.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         vendor.description?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = vendorFilter === 'all' || vendor.name.toUpperCase().includes(vendorFilter.toUpperCase());
    return matchesSearch && matchesFilter;
  });

  if (loading) return <div className="loading">Loading vendors...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="vendor-list">
      <h2>Choose a Certification Vendor</h2>
      <div className="vendor-grid">
        {filteredVendors.map(vendor => (
          <div
            key={vendor.id}
            className="vendor-card"
            onClick={() => onVendorSelect(vendor)}
          >
            <h3>{vendor.name}</h3>
            <p>{vendor.description || 'Professional certification provider'}</p>
            <div className="card-arrow">→</div>
          </div>
        ))}
      </div>
      {filteredVendors.length === 0 && (
        <div className="no-results">No vendors found matching your criteria.</div>
      )}
    </div>
  );
}

export default VendorList;