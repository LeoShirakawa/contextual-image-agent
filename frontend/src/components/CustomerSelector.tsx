"use client";

import { Customer } from "@/lib/bigquery";

const STYLE_COLORS: Record<string, string> = {
  "Modern Minimalist": "bg-gray-100 text-gray-800 border-gray-300",
  Industrial: "bg-amber-100 text-amber-800 border-amber-300",
  Bohemian: "bg-orange-100 text-orange-800 border-orange-300",
  Japandi: "bg-indigo-100 text-indigo-800 border-indigo-300",
  "Coastal Living": "bg-sky-100 text-sky-800 border-sky-300",
};

interface Props {
  customers: Customer[];
  selectedId: string;
  onSelect: (id: string) => void;
}

export default function CustomerSelector({
  customers,
  selectedId,
  onSelect,
}: Props) {
  const selected = customers.find((c) => c.customer_id === selectedId);

  return (
    <div className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center gap-4 flex-wrap">
          <span className="text-sm font-medium text-gray-500">
            Browsing as:
          </span>
          <div className="flex gap-2 flex-wrap">
            {customers.map((customer) => (
              <button
                key={customer.customer_id}
                onClick={() => onSelect(customer.customer_id)}
                className={`px-4 py-2 rounded-full text-sm font-medium border transition-all ${
                  selectedId === customer.customer_id
                    ? `${STYLE_COLORS[customer.style_preference] || "bg-gray-100"} ring-2 ring-offset-1 ring-gray-400`
                    : "bg-white text-gray-600 border-gray-200 hover:border-gray-400"
                }`}
              >
                {customer.name}
              </button>
            ))}
          </div>
          {selected && (
            <div className="ml-auto flex items-center gap-2 text-sm text-gray-500">
              <span
                className={`px-3 py-1 rounded-full text-xs font-medium border ${STYLE_COLORS[selected.style_preference] || ""}`}
              >
                {selected.style_preference}
              </span>
              <span className="hidden sm:inline">
                {selected.color_preference.join(", ")}
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
