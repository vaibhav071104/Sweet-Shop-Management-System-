import React, { useState, useEffect } from 'react';
import { Sweet } from '../types';
import { getSweets, searchSweets, createSweet, updateSweet, deleteSweet, purchaseSweet } from '../services/api';
import SweetCard from '../components/SweetCard';
import SweetForm from '../components/SweetForm';

interface DashboardProps {
  onLogout: () => void;
}

const Dashboard: React.FC<DashboardProps> = ({ onLogout }) => {
  const [sweets, setSweets] = useState<Sweet[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingSweet, setEditingSweet] = useState<Sweet | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const username = localStorage.getItem('username');

  useEffect(() => {
    fetchSweets();
  }, []);

  const fetchSweets = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await getSweets();
      setSweets(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('Failed to fetch sweets:', err);
      setError('Failed to load sweets');
      setSweets([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (searchTerm.trim()) {
      setLoading(true);
      setError('');
      try {
        const data = await searchSweets({ name: searchTerm });
        setSweets(Array.isArray(data) ? data : []);
      } catch (err) {
        console.error('Search failed:', err);
        setError('Search failed');
      } finally {
        setLoading(false);
      }
    } else {
      fetchSweets();
    }
  };

  const handleAddOrUpdateSweet = async (sweetData: Omit<Sweet, 'id'>) => {
    try {
      if (editingSweet) {
        await updateSweet(editingSweet.id, sweetData);
      } else {
        await createSweet(sweetData);
      }
      setShowForm(false);
      setEditingSweet(null);
      fetchSweets();
      alert('Success!');
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || error.message || 'Operation failed';
      alert(typeof errorMsg === 'string' ? errorMsg : 'Operation failed');
    }
  };

  const handlePurchase = async (id: number) => {
    try {
      await purchaseSweet(id, 1);
      fetchSweets();
      alert('Purchase successful!');
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || error.message || 'Purchase failed';
      alert(typeof errorMsg === 'string' ? errorMsg : 'Purchase failed');
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this sweet?')) {
      try {
        await deleteSweet(id);
        fetchSweets();
        alert('Deleted successfully!');
      } catch (error: any) {
        const errorMsg = error.response?.data?.detail || error.message || 'Delete failed';
        alert(typeof errorMsg === 'string' ? errorMsg : 'Delete failed');
      }
    }
  };

  const handleEdit = (sweet: Sweet) => {
    setEditingSweet(sweet);
    setShowForm(true);
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1> Sweet Shop Management</h1>
        <div className="header-actions">
          <span>Welcome, {username}!</span>
          <button className="btn-add" onClick={() => setShowForm(true)}>
            + Add Sweet
          </button>
          <button className="btn-logout" onClick={onLogout}>
            Logout
          </button>
        </div>
      </header>

      <div className="search-section">
        <input
          type="text"
          placeholder="Search sweets by name..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
        />
        <button onClick={handleSearch}>Search</button>
        <button onClick={() => { setSearchTerm(''); fetchSweets(); }}>Clear</button>
      </div>

      {error && <div className="error" style={{ margin: '20px 0' }}>{error}</div>}

      {loading ? (
        <div className="loading">Loading sweets...</div>
      ) : sweets.length === 0 ? (
        <div className="no-sweets">
          <p>No sweets available. Add some to get started!</p>
        </div>
      ) : (
        <div className="sweets-grid">
          {sweets.map((sweet) => (
            <SweetCard
              key={sweet.id}
              sweet={sweet}
              onPurchase={handlePurchase}
              onEdit={handleEdit}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}

      {showForm && (
        <SweetForm
          sweet={editingSweet}
          onSubmit={handleAddOrUpdateSweet}
          onCancel={() => {
            setShowForm(false);
            setEditingSweet(null);
          }}
        />
      )}
    </div>
  );
};

export default Dashboard;
