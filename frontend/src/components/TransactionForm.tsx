import React, { useState } from "react";
import { createTransaction } from "../services/api";

const TransactionForm = () => {
  const [form, setForm] = useState({
    customer_id: "",
    amount: 0,
    merchant: "",
    location: "",
    timestamp: new Date().toISOString(),
  });

  const handleSubmit = async () => {
    const res = await createTransaction(form);
    alert(`Fraud: ${res.data.fraud_flagged}, Risk: ${res.data.risk.risk_level}`);
  };

  return (
    <div>
      <h2>Add Transaction</h2>
      <input placeholder="Customer ID" onChange={e => setForm({...form, customer_id: e.target.value})}/>
      <input type="number" placeholder="Amount" onChange={e => setForm({...form, amount: Number(e.target.value)})}/>
      <input placeholder="Merchant" onChange={e => setForm({...form, merchant: e.target.value})}/>
      <input placeholder="Location" onChange={e => setForm({...form, location: e.target.value})}/>
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
};

export default TransactionForm;