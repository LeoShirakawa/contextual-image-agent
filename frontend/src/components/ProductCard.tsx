"use client";

import Link from "next/link";
import { Product } from "@/lib/bigquery";
import { BUCKET_NAME } from "@/lib/config";

interface Props {
  product: Product;
  customerId: string;
}

export default function ProductCard({ product, customerId }: Props) {
  const imagePath = product.image_gcs_uri.replace(
    `gs://${BUCKET_NAME}/`,
    ""
  );

  return (
    <Link
      href={`/products/${product.product_id}?customer=${customerId}`}
      className="group bg-white rounded-xl border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow"
    >
      <div className="aspect-square bg-gray-50 relative overflow-hidden">
        <img
          src={`/api/images?path=${encodeURIComponent(imagePath)}`}
          alt={product.name}
          className="w-full h-full object-contain p-4 group-hover:scale-105 transition-transform duration-300"
        />
      </div>
      <div className="p-4">
        <p className="text-xs text-gray-400 uppercase tracking-wide">
          {product.category}
        </p>
        <h3 className="font-semibold text-gray-900 mt-1 group-hover:text-blue-600 transition-colors">
          {product.name}
        </h3>
        <p className="text-sm text-gray-500 mt-1">{product.color}</p>
        <p className="text-lg font-bold text-gray-900 mt-2">
          ${product.price.toLocaleString()}
        </p>
        <div className="flex gap-1 mt-2 flex-wrap">
          {product.style_tags.map((tag) => (
            <span
              key={tag}
              className="text-xs px-2 py-0.5 bg-gray-100 text-gray-600 rounded-full"
            >
              {tag}
            </span>
          ))}
        </div>
      </div>
    </Link>
  );
}
