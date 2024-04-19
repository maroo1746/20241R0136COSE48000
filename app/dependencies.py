from app.database import SessionLocal, get_vectorstore as _get_vectorstore


def get_db():
    with SessionLocal() as db:
        try:
            yield db
            db.commit()
        except:
            db.rollback()
            raise


def get_vectorstore():
    return _get_vectorstore()
