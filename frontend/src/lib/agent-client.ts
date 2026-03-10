import { GoogleAuth } from "google-auth-library";
import {
  PROJECT_ID,
  AGENT_ENGINE_RESOURCE_ID,
  AGENT_ENGINE_LOCATION,
} from "./config";

const auth = new GoogleAuth({
  scopes: ["https://www.googleapis.com/auth/cloud-platform"],
});

function getBaseUrl(): string {
  return `https://${AGENT_ENGINE_LOCATION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${AGENT_ENGINE_LOCATION}/reasoningEngines/${AGENT_ENGINE_RESOURCE_ID}`;
}

async function getAccessToken(): Promise<string> {
  const client = await auth.getClient();
  const tokenResponse = await client.getAccessToken();
  return tokenResponse.token || "";
}

export async function createSession(
  userId: string,
  state?: Record<string, string>
): Promise<string> {
  const token = await getAccessToken();
  const res = await fetch(`${getBaseUrl()}:query`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      class_method: "async_create_session",
      input: { user_id: userId, ...(state ? { state } : {}) },
    }),
  });
  const data = await res.json();
  return data.output.id;
}

export interface AgentResponse {
  imageGcsUri?: string;
  styleNotes?: string;
  text?: string;
}

export async function streamQuery(
  userId: string,
  sessionId: string,
  message: string
): Promise<AgentResponse> {
  const token = await getAccessToken();
  const res = await fetch(`${getBaseUrl()}:streamQuery?alt=sse`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      class_method: "async_stream_query",
      input: {
        user_id: userId,
        session_id: sessionId,
        message,
      },
    }),
  });

  const sseText = await res.text();
  const result: AgentResponse = {};

  // Parse SSE events to find the final agent response
  const events = sseText.split("\n\n").filter((e) => e.trim());
  for (const event of events) {
    const dataLine = event
      .split("\n")
      .find((line) => line.startsWith("data:"));
    if (!dataLine) continue;
    try {
      const data = JSON.parse(dataLine.replace("data:", "").trim());
      const parts = data.content?.parts || data.parts;
      if (parts) {
        for (const part of parts) {
          if (part.text) {
            const text = part.text;
            // Extract GCS URI from text
            const gcsMatch = text.match(
              /gs:\/\/ctx-image-agent-\d+\/generated\/[^\s`'"]+/
            );
            if (gcsMatch) {
              result.imageGcsUri = gcsMatch[0];
            }
            // Extract style notes
            const styleMatch = text.match(
              /Style Notes?:?\s*(.+?)(?:\n|$)/i
            );
            if (styleMatch) {
              result.styleNotes = styleMatch[1].trim();
            }
            result.text = text;
          }
        }
      }
    } catch {
      // Skip non-JSON SSE events
    }
  }

  return result;
}
