"""
This file is for testing the quiz store
"""




######################################################
# unit tests, no http calls are made
######################################################

def t1():
    # tests does_quiz_exist() routine
    from app import does_quiz_exist
    case1 = does_quiz_exist("Super Science Quiz")
    print(f"True|{case1}")

    case2 = does_quiz_exist("some nonsense")
    print(f"False|{case2}")











def main():
    print("Expected|Got")
    print("----------------")
    t1()


if __name__ == '__main__':
    main()
