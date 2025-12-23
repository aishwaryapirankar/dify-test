# MongoDB Dify Integration Backend

This repository provides a Flask-based API bridge to connect **Dify.ai** with a **MongoDB** backend. It is designed to handle precise database operations while enforcing business logic guardrails directly at the API level.

## Evaluation Use-Cases & Features

The system is configured to support seven core evaluation scenarios:

1.  **Real-Time Product Lookup**: Execute queries to verify inventory and SKU details.
2.  **Lead Capture Storage**: Store marketing leads with automated phone format validation.
3.  **Order Management**: Update delivery status or perform safe deletions using filters.
4.  **Customer Segmentation**: Execute multi-stage aggregation pipelines for high-value customer analysis.
5.  **Chat Memory Retrieval**: Fetch sorted conversation history with specific limits and timestamp sorting.
6.  **Form-Based Workflow**: Reliable submission and retrieval of insurance request forms.
7.  **Status-Based Protection**: Logic-level protection that blocks updates to tickets already marked as "Closed".

## Tech Stack

* **Runtime**: Python 3.9
* **Web Framework**: Flask
* **Database**: MongoDB Atlas (via `pymongo`)
* **Infrastructure**: Railway (configured for `0.0.0.0` binding)
* **AI Orchestrator**: Dify.ai (Agentic Workflow)

## Setup & Configuration

### 1. Environment Variables
Set the following variables in your Railway dashboard or `.env` file:
* `DB_USERNAME`: Your MongoDB Atlas username.
* `DB_PASSWORD`: Your MongoDB Atlas password.

### 2. Dify OpenAPI YAML
Ensure the `servers.url` in your Dify tool configuration matches your Railway public URL. Use the provided `openapi.yaml` to register the `POST` endpoints.

## API Documentation

| Route | Method | Description |
| :--- | :--- | :--- |
| `/db/query` | `POST` | General search with `filter`, `sort`, and `limit`. |
| `/db/insert` | `POST` | Document insertion, includes `leads` phone validation. |
| `/db/update` | `POST` | Update documents, blocks updates for "Closed" tickets. |
| `/db/delete` | `POST` | Deletes a single document based on a filter. |
| `/db/aggregate` | `POST` | Runs a MongoDB aggregation pipeline array. |
