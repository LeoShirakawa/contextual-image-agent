# Implementation Plan: The Contextual Image Agent

## Overview
Multi-agent system that dynamically generates personalized product images
tailored to each customer's style preferences, deployed on Google Cloud.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15 (App Router) on Cloud Run |
| Backend | ADK (Python) deployed to Agent Engine (Vertex AI) |
| Orchestration LLM | Gemini 2.5 Flash |
| Image Generation | Gemini 3 Pro Image (`gemini-3-pro-image-preview`) |
| Structured Data | BigQuery |
| Unstructured Data | Cloud Storage |
| GCP Project | `tactile-octagon-372414` |
| Region | `us-central1` |

## Architecture

```
[Browser] --> [Next.js (Cloud Run)]
                    |
            [Next.js API Routes (BFF)]
                    |
        [Agent Engine (Vertex AI)]
        +---------------------------+
        |  Experience Orchestrator  | <-- SequentialAgent
        |  +- Customer Analyst      | --> BigQuery
        |  +- Product Analyst       | --> BigQuery + GCS
        |  +- Prompt Synthesizer    | --> BigQuery + GCS
        |  +- Image Generator       | --> Gemini 3 Pro Image --> GCS
        +---------------------------+
```

## Data: BigQuery dataset `contextual_image_agent`

Tables: customers, browsing_history, purchases, wishlists, products, brand_assets, generated_images

## Data: GCS bucket `ctx-image-agent-781890406104`

Folders: products/, brand-assets/, generated/

## Implementation Order

1. Phase 1: GCS bucket + BigQuery dataset/tables + seed data + image generation
2. Phase 2: ADK agents + tools + Agent Engine deploy
3. Phase 3: Next.js frontend + Cloud Run deploy
4. Phase 4: Integration test
