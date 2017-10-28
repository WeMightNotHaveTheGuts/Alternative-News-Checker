def main():
    InputData = ArticleInput()
    CheckArticle = ArticleChecker(InputData)
    status = returnStatus()

def ArticleInput():
    UserInput = input("Enter in fake news article: ")
    return UserInput

def returnStatus():
    return "Unknown"

def ArticleChecker(data):
    if '''"''' 

main()
