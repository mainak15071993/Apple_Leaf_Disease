FROM continuumio/anaconda3:latest
RUN pip freeze > req.txt
WORKDIR /home
COPY . /home
CMD ["python3", "app.py"]
 
