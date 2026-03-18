import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function CertificationList() {
  const { vendorId } = useParams();
  const [certifications, setCertifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:8000/vendor/${vendorId}/certifications`)
      .then(response => response.json())
      .then(data => {
        setCertifications(data);
        setLoading(false);
      })
      .catch(error => {
        setError(error.message);
        setLoading(false);
      });
  }, [vendorId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>Certifications</h2>
      <ul>
        {certifications.map(cert => (
          <li key={cert.id}>
            <a href={`/certification/${cert.id}`}>{cert.name}</a>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default CertificationList;