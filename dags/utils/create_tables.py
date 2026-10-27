from utils.models import Base
from utils.database import engine

Base.metadata.create_all(engine)

print("Таблицы успешно созданы!")