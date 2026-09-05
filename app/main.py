from fastapi import FastAPI
# from app.config import settings
from contextlib import asynccontextmanager
from app.exceptions.handler import unexcepted_exception_handler, integrity_error_handler
from sqlalchemy.exc import IntegrityError
from app.auth.router import auth_router
from app.donors.router import donor_router
from app.donations.router import donation_router
from app.admin.router import admin_router
from app.database import engine, create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to database and create tables
    try:
        with engine.connect() as connection:
            print("Database connected successfully")

        create_tables()
        print("Database tables created/verified successfully")

        yield

    except Exception as e:
        print(f"Database startup error: {e}")
        raise

    finally:
        engine.dispose()
        print("Database connection pool closed")


app = FastAPI(
    lifespan=lifespan,
    description="Madarsa fundraising system",
    version='0.1',

)
#error handling
app.add_exception_handler( Exception, unexcepted_exception_handler )
app.add_exception_handler(IntegrityError,integrity_error_handler)

#routers

app.include_router(auth_router)
app.include_router(donor_router)
app.include_router(donation_router)
app.include_router(admin_router)

# print(settings.DATABASE_URL)
@app.get("/")
def hello():
    return {
        "message" : "Hello From Madarsha Raza E Gaus"
    }