import os

"""
    This piece of code analyze basic properties of the dataset for Toutiao QA competition.
    It also trains a Logistic regression model as a baseline.

    Input data path: ~/../data/{invited_info_train, question_info, user_info, validate_nolabel}.txt

    @author: xinghai
"""

# load file and extract features for users and questions
curPath = os.path.dirname(os.path.realpath(__file__))
dataPath = curPath + "/../../data/"

class User:
    userMap = dict()
    numOfUniqueTags = 0

    def __init__(self, tags = None, description = None):
        self.tags = tags
        self.description = description
        User.numOfUniqueTags = max(User.numOfUniqueTags, max(tags))

    def to_string(self):
        ", ".join(self.tags)

    @staticmethod
    def get_num_of_user():
        return len(User.userMap)

    @staticmethod
    def parse_tags(tag_string):
        return [int(x) for x in tag_string.split("/")]

    @staticmethod
    def parse_description(description_string):
        # TODO: implement tag clustering algorithm, like LDA
        return []

    @staticmethod
    def addUser(user_id, user):
        User.userMap[user_id] = user

    @staticmethod
    def get_num_of_unique_tags:
        return User.numOfUniqueTags

    @staticmethod
    def get_user(user_id):
        return User.userMap[user_id]


with open(dataPath + "user_info.txt", "r") as fUser:
    for line in fUser:
        arr = line.split("\t")
        userId = arr[0]
        tags = User.parse_tags(arr[1])
        descriptions = User.parse_description(arr[2])
        User.addUser(userId, User(tags=tags, description=descriptions))
fUser.close()


class Question:
    questionMap = dict()
    numOfUniqueTags = 0

    def __init__(self, tag, words, numUpvotes, numAns, numTopQualAns):
        self.tag = tag
        self.words = words
        self.numUpvotes = numUpvotes
        self.numAns = numAns
        self.numTopQualAns = numTopQualAns
        User.numOfUniqueTags = max(User.numOfUniqueTags, tag)

    def to_string(self):
        return str(tag) + ", " + str(numUpvotes) + ", " + str(numAns) + ", " + str(numTopQualAns)

    @staticmethod
    def get_number_of_question():
        return len(Question.questionMap)

    @staticmethod
    def parse_tags(tag_string):
        return [int(x) for x in tag_string.split("/")]

    @staticmethod
    def parse_words(words):
        # TODO: implement some words understanding and clustering algorithms, like word2vec or LDA
        return []

    @staticmethod
    def add_question(questionId, question):
        Question.questionMap[questionId] = question

    @staticmethod
    def get_num_of_unique_tags:
        return Question.numOfUniqueTags

    @staticmethod
    def get_question(question_id):
        return Question.questionMap[question_id]

with open(dataPath + "question_info.txt", "r") as fQues:
    for line in fQues:
        arr = line.split("\t")
        questId = arr[0]
        tag = int(arr[1])
        words = arr[2]
        numUpvotes = int(arr[4])
        numAns = int(arr[5])
        numTopQualAns = int(arr[6])
        Question.add_question(questId, Question(tag=tag, words=words, numUpvotes=numUpvotes, numAns=numAns, numTopQualAns=numTopQualAns))
fQues.close()

class ModelData:
    numberOfData = 0

    def __init__(self, question_id, user_id, ans_or_not):
        self.questionId = question_id
        self.userId = user_id
        self.ansOrNot = ans_or_not

    def toString(self):
        questionFeature = Question.get_question(self.questionId).to_string()
        userFeature = User.get_user(self.userId).to_string()
        return self.questionId + ", " + self.userId + ", " + str(self.ansOrNot)

with open(dataPath + "invited_info_train.txt", "r") as fScoreMap:
    for line in fScoreMap:
        arr = line.split("\t")
        questionId = arr[0]
        userId = arr[1]
        ansOrNot = arr[2]
        ModelData(question_id=questionId, user_id=userId, ans_or_not=ansOrNot).toString()