import math
from typing import Generic, TypeVar, List, Dict, Any
from pydantic import BaseModel, Field

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    count: int
    total_pages: int
    current_page: int
    data: List[T]

def paginate(query, page: int = 1, per_page: int = 20) -> dict:
    total_count = query.count()
    total_pages = math.ceil(total_count / per_page) if per_page > 0 else 0
    
    if page < 1:
        page = 1
        
    offset = (page - 1) * per_page
    items = query.offset(offset).limit(per_page).all()
    
    return {
        "count": total_count,
        "total_pages": total_pages,
        "current_page": page,
        "data": items
    }
