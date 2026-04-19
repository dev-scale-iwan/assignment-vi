from sqlmodel import create_engine, Session

# engine = create_engine("sqlite:///iwansusanto.db", echo=True)
engine = create_engine("sqlite:///iwansusanto.db", connect_args={"timeout": 30})

def get_db():
    with Session(engine) as session:
        yield session