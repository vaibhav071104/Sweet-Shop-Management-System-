import React, { useState, useEffect } from 'react';
import './App.css';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './pages/Dashboard';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showRegister, setShowRegister] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleAuthSuccess = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    setIsAuthenticated(false);
  };

  if (isAuthenticated) {
    return <Dashboard onLogout={handleLogout} />;
  }

  return (
    <div className="App">
      <div className="auth-container">
        {showRegister ? (
          <Register
            onSuccess={handleAuthSuccess}
            onSwitchToLogin={() => setShowRegister(false)}
          />
        ) : (
          <Login
            onSuccess={handleAuthSuccess}
            onSwitchToRegister={() => setShowRegister(true)}
          />
        )}
      </div>
    </div>
  );
}

export default App;
