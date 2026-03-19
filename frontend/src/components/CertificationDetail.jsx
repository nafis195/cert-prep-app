import React from 'react';

function CertificationDetail({ certification }) {
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

  return (
    <div className="certification-detail">
      <div className="detail-header">
        <h1>{certification.name}</h1>
        <code className="exam-code-large">{certification.exam_code}</code>
      </div>

      <div className="detail-meta">
        <span
          className="difficulty-badge-large"
          style={{ backgroundColor: getDifficultyColor(certification.difficulty) }}
        >
          {certification.difficulty}
        </span>
        <div className="rating-large">
          {renderStars(4)}
          <span className="rating-text-large">(4.2 / 5.0)</span>
        </div>
      </div>

      <div className="detail-content">
        <div className="detail-section">
          <h3>Description</h3>
          <p>{certification.description || certification.summary || 'Detailed information about this certification.'}</p>
        </div>

        {certification.official_url && (
          <div className="detail-section">
            <h3>Official Resources</h3>
            <a
              href={certification.official_url}
              target="_blank"
              rel="noopener noreferrer"
              className="official-link"
            >
              View Official Certification Page →
            </a>
          </div>
        )}

        <div className="detail-section">
          <h3>Rate This Certification</h3>
          <div className="rating-input">
            <div className="stars-input">
              {[1, 2, 3, 4, 5].map(num => (
                <button key={num} className="star-btn">
                  ★
                </button>
              ))}
            </div>
            <textarea
              placeholder="Share your experience with this certification..."
              className="rating-comment"
            ></textarea>
            <button className="submit-rating-btn">Submit Rating</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CertificationDetail;