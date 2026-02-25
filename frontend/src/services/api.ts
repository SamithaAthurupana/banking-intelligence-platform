import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000/api",
});

export const createTransaction = (data: any) =>
  API.post("/transactions", data);

export const getCustomerAnalytics = (customerId: string) =>
  API.get(`/customers/${customerId}/analytics`);