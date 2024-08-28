import React, { useEffect, useState } from 'react';
import { io } from 'socket.io-client';

const socket = io(process.env.REACT_APP_API_URL, {
  path: process.env.REACT_APP_SOCKET_PATH,
});

export const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState({});
  
  useEffect(() => {
    socket.on('connect', () => {
      console.log('Connected to Socket.IO');
    });

    socket.on('disconnect', () => {
      console.log('Disconnected from Socket.IO');
    });

    socket.on('leaderboard_update', (data) => {
      setLeaderboard(data);
    });

    return () => {
      socket.off('leaderboard_update');
    };
  }, []);

  const handleScoreUpdate = (level, group, playerId) => {
    // Prompt user for score change amount
    const change = parseInt(prompt("Enter the score change amount:"), 10);

    if (!isNaN(change)) {
      // Emit event to update the player's score
      socket.emit('update_score', {
        level,
        group,
        playerId,
        change,
      });
    }
  };

  return (
    <div>
      <h2>Leaderboard</h2>
      {Object.entries(leaderboard).map(([level, groups]) => (
        <div key={level}>
          <h3>{level}</h3>
          {Object.entries(groups).map(([group, players]) => (
            <div key={group}>
              <h4>{group}</h4>
              <ul>
                {players.map((player) => (
                  <li key={player.id}>
                    {player.name}: {player.score}
                    <button
                      onClick={() => handleScoreUpdate(level, group, player.id)}
                      style={{ marginLeft: '10px' }}
                    >
                      Update Score
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};
