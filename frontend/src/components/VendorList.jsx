import React, { useState, useEffect } from 'react';

function VendorList() {
  const [vendors, setVendors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/vendors') // Adjust URL as needed
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

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>Vendors</h2>
      <ul>
        {vendors.map(vendor => (
          <li key={vendor.id}>
            <a href={`/vendor/${vendor.id}`}>{vendor.name}</a>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default VendorList;