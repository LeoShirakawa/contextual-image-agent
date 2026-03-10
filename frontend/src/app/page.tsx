"use client";

import { useState, useEffect } from "react";
import CustomerSelector from "@/components/CustomerSelector";
import ProductCard from "@/components/ProductCard";
import { Customer, Product } from "@/lib/bigquery";

export default function Home() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedCustomer, setSelectedCustomer] = useState("C001");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [customersRes, productsRes] = await Promise.all([
          fetch("/api/customers"),
          fetch("/api/products"),
        ]);
        setCustomers(await customersRes.json());
        setProducts(await productsRes.json());
      } catch (error) {
        console.error("Failed to load data:", error);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-gray-900">
              The Contextual Image Agent
            </h1>
            <p className="text-sm text-gray-500">
              AI-powered personalized product imagery
            </p>
          </div>
          <div className="flex items-center gap-2 px-3 py-1.5 bg-green-50 border border-green-200 rounded-full">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span className="text-xs font-medium text-green-700">
              Powered by Gemini 3
            </span>
          </div>
        </div>
      </header>

      {/* Customer Selector */}
      <CustomerSelector
        customers={customers}
        selectedId={selectedCustomer}
        onSelect={setSelectedCustomer}
      />

      {/* Product Grid */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <h2 className="text-lg font-semibold text-gray-900 mb-6">
          Product Catalog
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
          {products.map((product) => (
            <ProductCard
              key={product.product_id}
              product={product}
              customerId={selectedCustomer}
            />
          ))}
        </div>
      </main>
    </div>
  );
}
