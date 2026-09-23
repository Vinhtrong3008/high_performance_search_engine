from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Trong production, thay bằng domain cụ thể của bạn (ví dụ: ["https://yourdomain.com"])
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )