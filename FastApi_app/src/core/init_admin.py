from sqlalchemy import select
from src.core.database import get_async_session
from src.core.security import get_password_hash
from src.infrastructure.sqlite.models.users import User
from src.core.logger import logger


async def init_admin():
    print("init_admin: начало работы")
    async for session in get_async_session():
        try:
            print("Проверяем наличие админа...")
            result = await session.execute(select(User).where(User.login == "admin"))
            admin = result.scalar_one_or_none()
            
            if not admin:
                print("Админ не найден, создаём...")
                admin = User(
                    login="admin",
                    password=get_password_hash("admin123"),
                    is_admin=True
                )
                session.add(admin)
                await session.commit()
                logger.info("Администратор создан: admin / admin123")
                print("Администратор создан")
            else:
                print("Админ уже существует")
                logger.info("Администратор уже существует")
        except Exception as e:
            print(f"Ошибка: {e}")
            logger.error(f"Ошибка при создании админа: {e}")
        finally:
            break