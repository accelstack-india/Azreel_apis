from utils.constants import Constants


class ResponseBuilder:
    @staticmethod
    def loginResponseBuilder(user):
        responseObj = {
            "first_name": user[1],
            "last_name": user[2],
            "phone": user[3],
            "age": user[4],
            "email": user[5],
            "banuba_token": Constants.BANUBA_TOKEN
        }
        return responseObj
