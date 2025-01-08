from agent import EducationalBot

    
def main():
    query=input("How can I help you??")
    abot=EducationalBot()
    print(abot.query(query))

if __name__=="__main__":
    main()