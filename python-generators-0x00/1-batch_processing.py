from seed import connect_to_prodev
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models import User


def stream_users_in_batches(batch_size):
    
    engine = connect_to_prodev()
    Session = sessionmaker(bind=engine)
    session = Session()

    with Session() as session:
        counter = 0
        stmt = select(User)
        user_obj = session.scalars(stmt)
        for user in user_obj:
            counter += 1
            if counter > batch_size:
                break
            yield {
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email,
                'age': user.age
            }            


def batch_processing(batch_size):

    engine = connect_to_prodev()
    Session = sessionmaker(bind=engine)
    session = Session()

    with Session() as session:
        counter = 0
        stmt = select(User)
        user_obj = session.scalars(stmt)
        for user in user_obj:
            counter += 1
            if counter > batch_size:
                break
            if user.age <= 25:
                if counter > 0:
                    counter -= 1
                continue
            yield {
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email,
                'age': user.age
            }            




if __name__ == '__main__':
    
    for user in batch_processing(2):
        print(user)
