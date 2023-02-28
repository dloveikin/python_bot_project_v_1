from data_base.ORM.models import *


async def create_table():
    if db:
        db.create_tables([User])
        db.create_tables([Job])
        db.create_tables([Education])
        print("successfully create ORM tables")


async def base_start():
    print("\nsuccessfully connection to ORM database")
    await create_table()


async def orm_add_data(state):
    async with state.proxy() as data:

        usr = User.select().where(User.login == data["login"])
        print(usr)
        if len(usr) == 0:
            User(
                login=data["login"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                phone_number=data["phone_number"],
                mail=data["mail"],
                vacantion=data["vacantion"],
                photo_id=data["photo_id"]).save()
            print("successfully record to DB")
        else:
            query = User.update({
                User.first_name: data["first_name"],
                User.last_name: data["last_name"],
                User.phone_number: data["phone_number"],
                User.mail: data["mail"],
                User.vacantion: data["vacantion"],
                User.photo_id: data["photo_id"]}).where(User.login == data["login"])
            query.execute()


async def orm_delete_data(login):
    if len(User.select().where(User.login == login)) > 0:
        info = "ok"
        remove = User.delete().where(User.login == login)
        remove.execute()
        return info
    else:
        return None


async def orm_get_data(login):
    if len(User.select().where(User.login == login)) > 0:
        usr = User.get(User.login == login)
        return usr
    else:
        return None


async def orm_add_job(state):
    async with state.proxy() as data:
        print(data.keys())
        usr = User.select().where(User.login == data["login"])
        if len(usr) != 0:
            # state Job > state login > ForeignKeyField user_id to Users > User.id = job(login state)
            usr_id = int(User.get(User.login == data["login"]).id)

            Job(
                #
                user=usr_id,
                position=data["position"],
                years=data["years"],
                description=data["description"]).save()
            print("successfully record job to DB")
        else:
            return None


async def orm_add_education(state):
    async with state.proxy() as edu:
        usr = User.select().where(User.login == edu["login"])
        if len(usr) != 0:
            # state Edu > state login > ForeignKeyField user_id to Users > User.id = edu(login state)
            usr_id = int(User.get(User.login == edu["login"]).id)
            Education(
                user_id=usr_id,
                place=edu["place"],
                name=edu["name"],
                grade=edu["grade"]).save()
            print("successfully record education to DB")
        else:
            return None


async def select_all(login):
    print(login)
    user = User.get(User.login == login)
    educations = [education for education in Education.select().where(Education.user == user.id)]
    print(educations)
    jobs = [job for job in Job.select().where(Job.user == user.id)]
    print(jobs)
    return user, educations, jobs
