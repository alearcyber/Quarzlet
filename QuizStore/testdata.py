example1 = {
  "name": "example1",
  "description": "An example quiz to demonstrate questions with only the answer given. Must grab false answers from other questions",
  "quiz": [
    {
      "question": "What is 5 + 6?",
      "answer": "11"
    },
    {
      "question": "What is 3 * 5?",
      "answer": "15"
    },
    {
      "question": "What does HTTP stand for?",
      "answer": "Hypertext Transfer Protocol"
    }
  ]
}




example2 = {
  "name": "example2",
  "description": "An example quiz to demonstrate questions with a set of 4 answers",
  "quiz": [
    {
      "question": "What is 5 + 6?",
      "correctanswer": "11",
      "badanswers": ["12", "13", "10"]
    },
    {
      "question": "What is 3 * 5?",
      "correctanswer": "15",
      "badanswers": ["20", "3", "16"]
    },
    {
      "question": "What does HTTP stand for?",
      "correctanswer": "Hypertext Transfer Protocol",
      "badanswers": ["Hyper Transfer Text Protocol", "He tasted the pineapple", "Helical Tangerine Tango Peach"]
    }
  ]
}




post_example = """
  curl -X GET localhost:5000/getquiz -H 'Content-Type: application/json' -d '{"name":"example1"}'
  """