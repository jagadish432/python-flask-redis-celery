# contains classes/models used in this project


class User:
    name = ''
    phone = ''
    password= ''
    id = ''

    def __init__(self, email):
        self.email = email


class Notify:
    created_at = ''
    scheduled_at = ''
    duration = 0
    status = 'Waiting'
    
    def __init__(self, message, user):
        self.message = message
        self.user_id = user.id


