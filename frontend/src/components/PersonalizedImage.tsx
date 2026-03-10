"use client";

import { useState, useEffect } from "react";

interface Props {
  customerId: string;
  productId: string;
  originalImageUrl: string;
}

export default function PersonalizedImage({
  customerId,
  productId,
  originalImageUrl,
}: Props) {
  const [personalizedUrl, setPersonalizedUrl] = useState<string | null>(null);
  const [styleNotes, setStyleNotes] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showPersonalized, setShowPersonalized] = useState(false);

  useEffect(() => {
    setPersonalizedUrl(null);
    setStyleNotes("");
    setError(null);
    setShowPersonalized(false);
    generateImage();
  }, [customerId, productId]);

  async function generateImage() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/generate-image", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ customerId, productId }),
      });
      const data = await res.json();
      if (data.error) {
        setError(data.error);
      } else if (data.imageUrl) {
        setPersonalizedUrl(data.imageUrl);
        setStyleNotes(data.styleNotes || "");
        setTimeout(() => setShowPersonalized(true), 100);
      }
    } catch (err) {
      setError("Failed to generate personalized image");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-4">
      <div className="aspect-square bg-gray-50 rounded-xl overflow-hidden relative">
        {/* Original image */}
        <img
          src={originalImageUrl}
          alt="Product"
          className={`w-full h-full object-contain p-6 absolute inset-0 transition-opacity duration-700 ${
            showPersonalized ? "opacity-0" : "opacity-100"
          }`}
        />

        {/* Personalized image */}
        {personalizedUrl && (
          <img
            src={personalizedUrl}
            alt="Personalized lifestyle"
            className={`w-full h-full object-cover absolute inset-0 transition-opacity duration-700 ${
              showPersonalized ? "opacity-100" : "opacity-0"
            }`}
          />
        )}

        {/* Loading overlay */}
        {loading && (
          <div className="absolute inset-0 bg-white/60 backdrop-blur-sm flex flex-col items-center justify-center">
            <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
            <p className="mt-4 text-sm font-medium text-gray-700">
              Generating an image tailored to your style...
            </p>
            <p className="mt-1 text-xs text-gray-400">
              This may take 15-30 seconds
            </p>
          </div>
        )}
      </div>

      {/* Toggle buttons */}
      {personalizedUrl && !loading && (
        <div className="flex gap-2">
          <button
            onClick={() => setShowPersonalized(false)}
            className={`px-4 py-2 text-sm rounded-lg border transition-colors ${
              !showPersonalized
                ? "bg-gray-900 text-white border-gray-900"
                : "bg-white text-gray-600 border-gray-200 hover:border-gray-400"
            }`}
          >
            Original
          </button>
          <button
            onClick={() => setShowPersonalized(true)}
            className={`px-4 py-2 text-sm rounded-lg border transition-colors ${
              showPersonalized
                ? "bg-blue-600 text-white border-blue-600"
                : "bg-white text-gray-600 border-gray-200 hover:border-gray-400"
            }`}
          >
            Personalized for You
          </button>
        </div>
      )}

      {/* Style notes */}
      {styleNotes && !loading && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-800">
            <span className="font-semibold">Style Note:</span> {styleNotes}
          </p>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}
    </div>
  );
}
