import React, { useState, useEffect } from 'react';
import { Sweet } from '../types';

interface SweetFormProps {
  sweet?: Sweet | null;
  onSubmit: (sweet: Omit<Sweet, 'id'>) => void;
  onCancel: () => void;
}

const SweetForm: React.FC<SweetFormProps> = ({ sweet, onSubmit, onCancel }) => {
  const [name, setName] = useState('');
  const [category, setCategory] = useState('');
  const [price, setPrice] = useState('');
  const [quantity, setQuantity] = useState('');
  const [description, setDescription] = useState('');

  useEffect(() => {
    if (sweet) {
      setName(sweet.name);
      setCategory(sweet.category);
      setPrice(sweet.price.toString());
      setQuantity(sweet.quantity.toString());
      setDescription(sweet.description || '');
    }
  }, [sweet]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      name,
      category,
      price: parseFloat(price),
      quantity: parseInt(quantity),
      description: description || undefined,
    });
  };

  return (
    <div className="sweet-form-overlay">
      <div className="sweet-form">
        <h3>{sweet ? 'Edit Sweet' : 'Add New Sweet'}</h3>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Sweet Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Category (e.g., Chocolate, Gummy)"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            required
          />
          <input
            type="number"
            step="0.01"
            placeholder="Price"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            required
          />
          <input
            type="number"
            placeholder="Quantity"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            required
          />
          <textarea
            placeholder="Description (optional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
          />
          <div className="form-actions">
            <button type="submit" className="btn-submit">
              {sweet ? 'Update' : 'Add'} Sweet
            </button>
            <button type="button" className="btn-cancel" onClick={onCancel}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SweetForm;
