import React, { useState, useEffect } from 'react';

function CertificationList({ vendor, onCertificationSelect, searchTerm }) {
  const [certifications, setCertifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:8000/vendor/${vendor.id}/certifications`)
      .then(response => response.json())
      .then(data => {
        setCertifications(data);
        setLoading(false);
      })
      .catch(error => {
        setError(error.message);
        setLoading(false);
      });
  }, [vendor.id]);

  const filteredCertifications = certifications.filter(cert =>
    cert.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    cert.exam_code.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'beginner': return '#10B981'; // green
      case 'intermediate': return '#F59E0B'; // yellow
      case 'advanced': return '#EF4444'; // red
      default: return '#6B7280'; // gray
    }
  };

  const renderStars = (rating) => {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      stars.push(
        <span key={i} className={`star ${i <= rating ? 'filled' : ''}`}>
          ★
        </span>
      );
    }
    return stars;
  };

  if (loading) return <div className="loading">Loading certifications...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="certification-list">
      <h2>{vendor.name} Certifications</h2>
      <div className="certification-grid">
        {filteredCertifications.map(cert => (
          <div
            key={cert.id}
            className="certification-card"
            onClick={() => onCertificationSelect(cert)}
          >
            <div className="cert-header">
              <h3>{cert.name}</h3>
              <code className="exam-code">{cert.exam_code}</code>
            </div>

            <div className="cert-meta">
              <span
                className="difficulty-badge"
                style={{ backgroundColor: getDifficultyColor(cert.difficulty) }}
              >
                {cert.difficulty}
              </span>
              <div className="rating">
                {renderStars(4)} {/* Placeholder rating - would come from backend */}
                <span className="rating-text">(4.2)</span>
              </div>
            </div>

            <p className="cert-summary">
              {cert.summary || 'Professional certification for career advancement.'}
            </p>

            <div className="card-arrow">→</div>
          </div>
        ))}
      </div>
      {filteredCertifications.length === 0 && (
        <div className="no-results">No certifications found matching your search.</div>
      )}
    </div>
  );
}

export default CertificationList;