import React, { useEffect, useState } from "react";
import { getCustomerAnalytics } from "../services/api";
import { BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";

const AnalyticsChart = ({ customerId }: { customerId: string }) => {
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    getCustomerAnalytics(customerId).then((res: any) => {
      const monthly = res.data.monthly_spending;
      const formatted = Object.keys(monthly).map(key => ({
        month: key,
        amount: monthly[key]
      }));
      setData(formatted);
    });
  }, [customerId]);

  return (
    <div>
      <h2>Monthly Spending</h2>
      <BarChart width={500} height={300} data={data}>
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="amount" />
      </BarChart>
    </div>
  );
};

export default AnalyticsChart;