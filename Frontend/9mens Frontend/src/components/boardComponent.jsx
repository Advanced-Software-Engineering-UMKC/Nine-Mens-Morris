import React, { useState } from 'react';
import '../App.css';

const points = [
  { id: 1, x: 0, y: 0 }, { id: 2, x: 3, y: 0 }, { id: 3, x: 6, y: 0 }, // Top row
  { id: 4, x: 1, y: 1 }, { id: 5, x: 3, y: 1 }, { id: 6, x: 5, y: 1 }, // Mid row
  { id: 7, x: 2, y: 2 }, { id: 8, x: 3, y: 2 }, { id: 9, x: 4, y: 2 }, // Inner row
  { id: 10, x: 0, y: 3 }, { id: 11, x: 1, y: 3 }, { id: 12, x: 2, y: 3 }, // Left side
  { id: 13, x: 4, y: 3 }, { id: 14, x: 5, y: 3 }, { id: 15, x: 6, y: 3 }, // Right side
  { id: 16, x: 2, y: 4 }, { id: 17, x: 3, y: 4 }, { id: 18, x: 4, y: 4 }, // Inner bottom row
  { id: 19, x: 1, y: 5 }, { id: 20, x: 3, y: 5 }, { id: 21, x: 5, y: 5 }, // Middle bottom row
  { id: 22, x: 0, y: 6 }, { id: 23, x: 3, y: 6 }, { id: 24, x: 6, y: 6 }, // Bottom row
];

// Define lines to connect points
const lines = [
  { start: 1, end: 2 }, { start: 2, end: 3 }, // Top row
  { start: 1, end: 10 }, { start: 3, end: 15 }, // Left and right verticals
  { start: 10, end: 22 }, { start: 15, end: 24 }, // Outer vertical lines
  { start: 22, end: 23 }, { start: 23, end: 24 }, // Bottom row
  // More connections between points can be defined here...
];

const GameBoard = () => {
  const [player, setPlayer] = useState('player1');
  const [board, setBoard] = useState(Array(24).fill(null)); // 24 positions

  const handleClick = (index) => {
    if (board[index] === null) {
      const newBoard = [...board];
      newBoard[index] = player;
      setBoard(newBoard);
      setPlayer(player === 'player1' ? 'player2' : 'player1');
    }
  };

  // Helper to get coordinates from a point id
  const getCoordinates = (id) => {
    const point = points.find(p => p.id === id);
    return point ? { x: point.x * 100 + 25, y: point.y * 100 + 25 } : null; // Offset for centering
  };

  return (
    <div className="board">
      <svg className="board-lines" viewBox="0 0 700 700" style={{ position: 'absolute', top: 0, left: 0 }} >
        {/* Render lines between points */}
        {lines.map((line, index) => {
          const startCoords = getCoordinates(line.start);
          const endCoords = getCoordinates(line.end);
          return startCoords && endCoords ? (
            <line
              key={index}
              x1={startCoords.x}
              y1={startCoords.y}
              x2={endCoords.x}
              y2={endCoords.y}
              stroke="black"
              strokeWidth="2"
            />
          ) : null;
        })}
      </svg>

      {/* Render points */}
      {points.map((point, index) => (
        <div
          key={point.id}
          className={`point ${board[index]}`}
          onClick={() => handleClick(index)}
          style={{ top: `${point.y * 100}px`, left: `${point.x * 100}px` }}
        >
          {board[index] && (
            <div className={`piece ${board[index]}`}>
              {board[index] === 'player1' ? 'P1' : 'P2'}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default GameBoard;
