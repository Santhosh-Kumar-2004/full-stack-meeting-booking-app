from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from helper.database import get_db
from schemas.booking import BookingCreate, BookingResponse
from models.models import Booking

router = APIRouter(prefix="/bookings", tags=["Bookings"])


# Create booking and this endppint is used by admin also user - 1
@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking: BookingCreate, 
    db: Session = Depends(get_db)
):
    """
    Creates a new booking record in the database.

    Accepts booking details and saves the new record, returning the created object.
    This endpoint is intended for both standard users and administrative use.

    Raises:
        HTTPException 500: Unexpected server or database error.
    """

    try:
        new_booking = Booking(
            user_id=booking.user_id,
            date=booking.date,
            time=booking.time,
            description=booking.description
        )
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        return new_booking
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating booking: {str(e)}"
        )


# Get all bookings and this endpoint is used by only admin - 2
@router.get("/", response_model=list[BookingResponse])
def get_bookings(
    db: Session = Depends(get_db)
):
    """
    Retrieves a list of all existing bookings.

    This endpoint is restricted for **Admin** use only.

    Returns:
        list[BookingResponse]: A list of all booking objects.

    Raises:
        HTTPException 500: Unexpected server or database error.
    """
    
    try:
        bookings = db.query(Booking).all()
        return bookings
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching bookings: {str(e)}"
        )


# Delete booking and this endpoint is used by only admin - 3
@router.delete("/{booking_id}", status_code=status.HTTP_200_NO_CONTENT)
def delete_booking(booking_id: str, db: Session = Depends(get_db)):
    try:
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        db.delete(booking)
        db.commit()
        return {"message": "Booking deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting booking: {str(e)}"
        )
