import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import Optional
from database import create_document
from schemas import Order

app = FastAPI(title="Papayow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Papayow Backend Running"}

@app.get("/test")
def test_database():
    from database import db
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            try:
                response["collections"] = db.list_collection_names()[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# Order submission with file upload
@app.post("/api/order")
async def submit_order(
    parent_email: EmailStr = Form(...),
    description: Optional[str] = Form(None),
    product_type: str = Form(...),
    photo: UploadFile = File(...),
):
    # Validate product type
    if product_type not in ["figurine", "coloring_book"]:
        raise HTTPException(status_code=400, detail="Invalid product_type")

    # Save uploaded file to disk in a temp/uploads directory
    upload_dir = os.path.join(os.getcwd(), "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    filename_safe = photo.filename.replace(" ", "_")
    file_path = os.path.join(upload_dir, filename_safe)

    with open(file_path, "wb") as f:
        f.write(await photo.read())

    # Create order document
    order = Order(
        parent_email=parent_email,
        description=description,
        product_type=product_type,  # type: ignore
        photo_filename=filename_safe,
    )

    try:
        order_id = create_document("order", order)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return {"message": "Order received", "order_id": order_id}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
