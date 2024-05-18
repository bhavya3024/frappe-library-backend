import sys
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import services.book
import services.charts
from utils.index import ResponseExecption
sys.path.append('../services/charts.py')

chartService = services.charts

router = APIRouter()


@router.get("/book-stats")
def get_book_stats():
    try:
        stats = chartService.get_book_stats()
        return JSONResponse({
           "success": True,
           "stats": jsonable_encoder(stats),
        })
    except ResponseExecption as e:
      print(e)
      raise HTTPException(status_code=e.status or 500 ,detail=e.message or "Internal Server Error")  

   
@router.get('/member-stats')
def total_members():
   try:
      stats = chartService.member_wise_rent_stats()
      return JSONResponse({
         "success": True,
         "stats": jsonable_encoder(stats)
      })
   except ResponseExecption as e:
      print(e)
      raise HTTPException(status_code=e.status or 500 ,detail=e.message or "Internal Server Error")