class TestConfig: 
    ENVIRONMENTS = { 
        "prod": "https://excursium.com/", 
        "stage": "https://excursium.com/", 
        "dev": "https://excursium.com/" 
    } 
 
    TEST_USERS = { 
        "admin": {"email": "aleskobelev@yandex.ru", "password": "34670Eks"}, 
        "user": {"email": "aleskobelev@yandex.ru", "password": "34670Eks"} 
    } 
 
    @classmethod 
    def get_base_url(cls, env="stage"): 
        return cls.ENVIRONMENTS.get(env, cls.ENVIRONMENTS["stage"]) 
 
    @classmethod 
    def get_user_credentials(cls, user_type="user"): 
        return cls.TEST_USERS.get(user_type, cls.TEST_USERS["user"]) 
