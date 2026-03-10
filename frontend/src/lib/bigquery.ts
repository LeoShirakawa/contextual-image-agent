import { BigQuery } from "@google-cloud/bigquery";
import { PROJECT_ID, DATASET_ID } from "./config";

const bigquery = new BigQuery({ projectId: PROJECT_ID });

export interface Customer {
  customer_id: string;
  name: string;
  email: string;
  style_preference: string;
  color_preference: string[];
  aesthetic_keywords: string[];
}

export interface Product {
  product_id: string;
  name: string;
  category: string;
  color: string;
  material: string;
  description: string;
  price: number;
  image_gcs_uri: string;
  style_tags: string[];
}

export async function getCustomers(): Promise<Customer[]> {
  const [rows] = await bigquery.query({
    query: `SELECT customer_id, name, email, style_preference, color_preference, aesthetic_keywords
            FROM \`${PROJECT_ID}.${DATASET_ID}.customers\`
            ORDER BY customer_id`,
  });
  return rows as Customer[];
}

export async function getProducts(): Promise<Product[]> {
  const [rows] = await bigquery.query({
    query: `SELECT product_id, name, category, color, material, description, price, image_gcs_uri, style_tags
            FROM \`${PROJECT_ID}.${DATASET_ID}.products\`
            ORDER BY product_id`,
  });
  return rows as Product[];
}

export async function getProduct(productId: string): Promise<Product | null> {
  const [rows] = await bigquery.query({
    query: `SELECT product_id, name, category, color, material, description, price, image_gcs_uri, style_tags
            FROM \`${PROJECT_ID}.${DATASET_ID}.products\`
            WHERE product_id = @productId`,
    params: { productId },
  });
  return rows.length > 0 ? (rows[0] as Product) : null;
}
