from fastapi import HTTPException
news_not_found = HTTPException(status_code=404, detail="News not found")
unauthorized_exception = HTTPException(status_code=403, detail="Unauthorized to perform this action")
