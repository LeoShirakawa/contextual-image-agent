import { NextRequest, NextResponse } from "next/server";
import { createSession, streamQuery } from "@/lib/agent-client";
import { AGENT_ENGINE_RESOURCE_ID } from "@/lib/config";

export async function POST(request: NextRequest) {
  try {
    const { customerId, productId } = await request.json();

    if (!customerId || !productId) {
      return NextResponse.json(
        { error: "Missing customerId or productId" },
        { status: 400 }
      );
    }

    if (!AGENT_ENGINE_RESOURCE_ID) {
      return NextResponse.json(
        { error: "Agent Engine not configured. Set AGENT_ENGINE_RESOURCE_ID." },
        { status: 503 }
      );
    }

    // Create a session for this request
    const sessionId = await createSession(customerId);

    // Send the personalization request
    const message = `Generate a personalized lifestyle image for customer ${customerId} viewing product ${productId}. The customer_id is ${customerId} and product_id is ${productId}.`;
    const result = await streamQuery(customerId, sessionId, message);

    return NextResponse.json({
      imageUrl: result.imageGcsUri
        ? `/api/images?path=${encodeURIComponent(result.imageGcsUri.replace("gs://ctx-image-agent-781890406104/", ""))}`
        : null,
      styleNotes: result.styleNotes || "",
      rawText: result.text || "",
    });
  } catch (error) {
    console.error("Error generating image:", error);
    return NextResponse.json(
      { error: "Failed to generate personalized image" },
      { status: 500 }
    );
  }
}
