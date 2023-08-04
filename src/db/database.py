from sqlalchemy import Column, Integer, create_engine, inspect
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_engine("sqlite:///price_lists.db")


def session_generator():
    return sessionmaker(bind=engine)


def session():
    if not inspect(engine).has_table("first_store"):
        Base.metadata.create_all(engine)

    try:
        get_session = session_generator()

        with get_session() as session:
            yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
