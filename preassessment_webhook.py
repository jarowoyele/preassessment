"""
Pre-assessment Webhook Receiver
Receives organization_id, preassessment_id, and regulation_id
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class PreassessmentWebhookPayload(BaseModel):
    """Expected webhook payload structure"""
    organization_id: str
    preassessment_id: str
    regulation_id: str

# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="Pre-assessment Webhook Receiver",
    description="Receives organization_id, preassessment_id, and regulation_id",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store received webhooks in memory
received_webhooks = []

@app.get("/")
async def root():
    return {
        "message": "Pre-assessment Webhook Receiver",
        "version": "1.0.0",
        "endpoint": "POST /webhook/preassessment"
    }

@app.post("/webhook/preassessment")
async def receive_preassessment_webhook(request: Request, payload: PreassessmentWebhookPayload):
    """
    Receive webhook for pre-assessment
    
    Expected payload:
    {
        "organization_id": "682ae94fa2e778c597d09b57",
        "preassessment_id": "507f1f77bcf86cd799439011",
        "regulation_id": "6981ea4cb358c36d4be852be"
    }
    """
    try:
        logger.info("=" * 80)
        logger.info("PRE-ASSESSMENT WEBHOOK RECEIVED")
        logger.info("=" * 80)
        logger.info(f"Timestamp: {datetime.utcnow().isoformat()}")
        logger.info(f"Organization ID: {payload.organization_id}")
        logger.info(f"Pre-assessment ID: {payload.preassessment_id}")
        logger.info(f"Regulation ID: {payload.regulation_id}")
        
        # Store webhook
        webhook_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "organization_id": payload.organization_id,
            "preassessment_id": payload.preassessment_id,
            "regulation_id": payload.regulation_id
        }
        
        received_webhooks.append(webhook_data)
        
        logger.info("=" * 80)
        logger.info("WEBHOOK RECEIVED SUCCESSFULLY")
        logger.info("=" * 80)
        
        return {
            "status": "success",
            "message": "Webhook received successfully",
            "received_at": datetime.utcnow().isoformat(),
            "payload": {
                "organization_id": payload.organization_id,
                "preassessment_id": payload.preassessment_id,
                "regulation_id": payload.regulation_id
            }
        }
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process webhook: {str(e)}"
        )

@app.get("/webhook/received")
async def get_received_webhooks():
    """View all received webhooks"""
    return {
        "total_received": len(received_webhooks),
        "webhooks": received_webhooks
    }

@app.delete("/webhook/received")
async def clear_received_webhooks():
    """Clear all received webhooks"""
    global received_webhooks
    count = len(received_webhooks)
    received_webhooks = []
    
    return {
        "status": "success",
        "message": f"Cleared {count} webhooks"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "webhooks_received": len(received_webhooks)
    }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 80)
    print("PRE-ASSESSMENT WEBHOOK RECEIVER")
    print("=" * 80)
    print("Server starting on: http://localhost:8008")
    print("Webhook endpoint: POST http://localhost:8008/webhook/preassessment")
    print("View received: GET http://localhost:8008/webhook/received")
    print("=" * 80 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8008)
