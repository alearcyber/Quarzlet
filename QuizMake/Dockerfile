#NOTE, THIS NEEDS TO BE FIXED FOR THE REFACTORING WHERE EVERYTHING WAS PUT INTO THE FOLDER
# TO RUN, YOU MUST CD INTO THE QuizStore PATH SO IT WORKS RIGHT.

#grab python image
FROM python:3.10-alpine

ENV PORT 8001

#move requirements into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

#copy necessary files
COPY app.py /app
COPY templates/ /app/templates
COPY static/ /app/static

EXPOSE $PORT

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

# parameter for the "ENTRYPOINT" above. Basically makes it run the application.
CMD ["app.py" ]
