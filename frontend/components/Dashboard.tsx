import React, { useState } from "react";
import TransactionForm from "./TransactionForm";
import AnalyticsChart from "./AnalyticsChart";

const Dashboard = () => {
  const [customerId, setCustomerId] = useState("C001");

  return (
    <div>
      <h1>Banking Intelligence Dashboard</h1>
      <TransactionForm />
      <input 
        placeholder="Customer ID for Analytics"
        onChange={e => setCustomerId(e.target.value)}
      />
      <AnalyticsChart customerId={customerId} />
    </div>
  );
};

export default Dashboard;