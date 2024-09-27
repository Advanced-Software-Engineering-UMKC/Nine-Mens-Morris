import React from 'react';
import './board.css';

function Board() {
  return (
    <div className="board-container">
      <div className="board">
        {/* SVG for lines */}
        <svg className="board-lines" viewBox="0 0 700 700">
          {/* Outer square */}
          <line x1="50" y1="50" x2="650" y2="50" />
          <line x1="50" y1="50" x2="50" y2="650" />
          <line x1="50" y1="650" x2="650" y2="650" />
          <line x1="650" y1="50" x2="650" y2="650" />
          
          {/* Middle square */}
          <line x1="150" y1="150" x2="550" y2="150" />
          <line x1="150" y1="150" x2="150" y2="550" />
          <line x1="150" y1="550" x2="550" y2="550" />
          <line x1="550" y1="150" x2="550" y2="550" />
          
          {/* Inner square */}
          <line x1="250" y1="250" x2="450" y2="250" />
          <line x1="250" y1="250" x2="250" y2="450" />
          <line x1="250" y1="450" x2="450" y2="450" />
          <line x1="450" y1="250" x2="450" y2="450" />
          
          {/* Connecting lines */}
          <line x1="50" y1="350" x2="250" y2="350" />
          <line x1="650" y1="350" x2="450" y2="350" />
          <line x1="350" y1="50" x2="350" y2="250" />
          <line x1="350" y1="650" x2="350" y2="450" />
        </svg>

   
        {/* Add remaining points similarly */}
      </div>
    </div>
  );
}

export default Board;
