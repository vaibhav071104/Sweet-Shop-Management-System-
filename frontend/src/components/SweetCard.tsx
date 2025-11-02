import React from 'react';
import { Sweet } from '../types';

interface SweetCardProps {
  sweet: Sweet;
  onPurchase: (id: number) => void;
  onEdit?: (sweet: Sweet) => void;
  onDelete?: (id: number) => void;
}

const SweetCard: React.FC<SweetCardProps> = ({ sweet, onPurchase, onEdit, onDelete }) => {
  return (
    <div className="sweet-card">
      <h3>{sweet.name}</h3>
      <span className="category">{sweet.category}</span>
      <p className="price">₹{sweet.price.toFixed(2)}</p>
      <p className={sweet.quantity === 0 ? 'out-of-stock' : 'in-stock'}>
        Stock: {sweet.quantity}
      </p>
      {sweet.description && <p className="description">{sweet.description}</p>}
      
      <div className="card-actions">
        <button
          className="btn-purchase"
          onClick={() => onPurchase(sweet.id)}
          disabled={sweet.quantity === 0}
        >
          {sweet.quantity === 0 ? 'Out of Stock' : 'Purchase'}
        </button>
        
        {onEdit && (
          <button className="btn-edit" onClick={() => onEdit(sweet)}>
            Edit
          </button>
        )}
        
        {onDelete && (
          <button className="btn-delete" onClick={() => onDelete(sweet.id)}>
            Delete
          </button>
        )}
      </div>
    </div>
  );
};

export default SweetCard;
