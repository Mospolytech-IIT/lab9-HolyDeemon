from dataclasses import dataclass

@dataclass
class User:
    id : int
    username : str
    email :str
    password:str
    def dictionary(self):
        return {"id" : self.id,
                "username" : self.username,
                "email" : self.email,
                "password" : self.password}

@dataclass
class Posts:
    id: int
    title: str
    content: str
    user_id: int
    def dictionary(self):
        return {"id" : self.id,
                "title" : self.title,
                "content" : self.content,
                "user_id" : self.user_id}


