"use client";

import { useState, useEffect, use } from "react";
import Link from "next/link";
import PersonalizedImage from "@/components/PersonalizedImage";
import CustomerSelector from "@/components/CustomerSelector";
import { Customer, Product } from "@/lib/bigquery";
import { BUCKET_NAME } from "@/lib/config";

export default function ProductDetailPage({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ customer?: string }>;
}) {
  const { id } = use(params);
  const { customer: customerParam } = use(searchParams);

  const [customers, setCustomers] = useState<Customer[]>([]);
  const [product, setProduct] = useState<Product | null>(null);
  const [selectedCustomer, setSelectedCustomer] = useState(
    customerParam || "C001"
  );
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [customersRes, productsRes] = await Promise.all([
          fetch("/api/customers"),
          fetch("/api/products"),
        ]);
        const customersData = await customersRes.json();
        const productsData = await productsRes.json();
        setCustomers(customersData);
        const found = productsData.find(
          (p: Product) => p.product_id === id
        );
        setProduct(found || null);
      } catch (error) {
        console.error("Failed to load data:", error);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!product) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-500">Product not found</p>
      </div>
    );
  }

  const originalImagePath = product.image_gcs_uri.replace(
    `gs://${BUCKET_NAME}/`,
    ""
  );
  const originalImageUrl = `/api/images?path=${encodeURIComponent(originalImagePath)}`;

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center gap-4">
          <Link
            href="/"
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
                clipRule="evenodd"
              />
            </svg>
          </Link>
          <div>
            <h1 className="text-xl font-bold text-gray-900">
              The Contextual Image Agent
            </h1>
            <p className="text-sm text-gray-500">
              AI-powered personalized product imagery
            </p>
          </div>
        </div>
      </header>

      {/* Customer Selector */}
      <CustomerSelector
        customers={customers}
        selectedId={selectedCustomer}
        onSelect={setSelectedCustomer}
      />

      {/* Product Detail */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
          {/* Left: Image */}
          <PersonalizedImage
            customerId={selectedCustomer}
            productId={product.product_id}
            originalImageUrl={originalImageUrl}
          />

          {/* Right: Product Info */}
          <div className="space-y-6">
            <div>
              <p className="text-sm text-gray-400 uppercase tracking-wide">
                {product.category}
              </p>
              <h2 className="text-3xl font-bold text-gray-900 mt-1">
                {product.name}
              </h2>
              <p className="text-2xl font-bold text-gray-900 mt-2">
                ${product.price.toLocaleString()}
              </p>
            </div>

            <div className="space-y-3">
              <div className="flex gap-2">
                <span className="text-sm font-medium text-gray-500 w-20">
                  Color
                </span>
                <span className="text-sm text-gray-900">{product.color}</span>
              </div>
              <div className="flex gap-2">
                <span className="text-sm font-medium text-gray-500 w-20">
                  Material
                </span>
                <span className="text-sm text-gray-900">
                  {product.material}
                </span>
              </div>
            </div>

            <p className="text-gray-600 leading-relaxed">
              {product.description}
            </p>

            <div className="flex gap-2 flex-wrap">
              {product.style_tags.map((tag) => (
                <span
                  key={tag}
                  className="text-xs px-3 py-1 bg-gray-100 text-gray-600 rounded-full"
                >
                  {tag}
                </span>
              ))}
            </div>

            <button className="w-full bg-gray-900 text-white py-3 rounded-lg font-medium hover:bg-gray-800 transition-colors">
              Add to Cart
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
