#NOTE, THIS NEEDS TO BE FIXED FOR THE REFACTORING WHERE EVERYTHING WAS PUT INTO THE FOLDER
# TO RUN, YOU MUST CD INTO THE QuizStore PATH SO IT WORKS RIGHT.

#grab python image
FROM python:3.10-alpine

#move requirements into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

#copy necissary files
COPY app.py /app
COPY templates/ /app/templates
COPY static/ /app/static
COPY app.py /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

# parameter for the "ENTRYPOINT" above. Basically makes it run the application.
CMD ["app.py" ]
