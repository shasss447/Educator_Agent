from agent import EducationalBot

    
def main():
    query=input("How can I help you??")
    bot=EducationalBot()
    print(bot(query))

if __name__=="__main__":
    main()