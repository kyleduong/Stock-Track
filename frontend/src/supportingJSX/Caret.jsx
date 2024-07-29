import React from 'react';

const Caret = ({ direction }) => {
  return (
    <span className="caret">
      {direction === "asc" ? (
        <svg width="20px" height="20px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M7 14L12 9L17 14H7Z" fill="currentColor"/>
        </svg>
      ) : (
        <svg width="20px" height="20px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M7 10L12 15L17 10H7Z" fill="currentColor"/>
        </svg>
      )}
    </span>
  );
};

export default Caret;