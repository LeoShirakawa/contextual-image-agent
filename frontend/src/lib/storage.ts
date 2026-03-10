import { Storage } from "@google-cloud/storage";
import { PROJECT_ID, BUCKET_NAME } from "./config";

const storage = new Storage({ projectId: PROJECT_ID });

export function gcsUriToPublicPath(gcsUri: string): string {
  // Convert gs://bucket/path to /api/images?path=path
  const path = gcsUri.replace(`gs://${BUCKET_NAME}/`, "");
  return `/api/images?path=${encodeURIComponent(path)}`;
}

export async function getImageBuffer(
  gcsPath: string
): Promise<{ buffer: Buffer; contentType: string }> {
  const bucket = storage.bucket(BUCKET_NAME);
  const file = bucket.file(gcsPath);
  const [buffer] = await file.download();
  return { buffer: Buffer.from(buffer), contentType: "image/png" };
}
