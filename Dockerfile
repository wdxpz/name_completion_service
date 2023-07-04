FROM python:3.10

WORKDIR /projects/name_completion_service
COPY . .

#install ROS dependency
RUN apt-get update \
#    && apt-get install -y “elasticsearch==7.0.0” requests djangorestframework \
    && rm -rf /var/lib/apt/lists/

#install requirements
RUN pip install elasticsearch==7.0.0 django djangorestframework requests

#build the .bashrc for bash file
#RUN /bin/bash -c "echo 'source /opt/ros/kinetic/setup.bash' >> /root/.bashrc

#add this and below command will run without cache
#ARG CACHEBUST=1

CMD ["python", "manage.py", "runserver", "0.0.0.0:8064"]
