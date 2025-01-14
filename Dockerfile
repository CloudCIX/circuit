FROM cloudcix/framework:4

WORKDIR /application_framework/circuit
COPY . .

# Install the requirements
RUN pip3 install -r requirements.txt \
   && mv urls_local.py /application_framework/system_conf/urls_local.py \
   && mv settings_local.py /application_framework/system_conf/settings_local.py \
   && mv /application_framework/training/errors /application_framework

WORKDIR /application_framework
EXPOSE 443

# Setup the entrypoint - Migrate the DB changes if there are any, and run gunicorn
ENTRYPOINT python3 manage.py migrate --database=circuit circuit \
   && gunicorn --preload 

# Genereate documentation 
RUN touch public-key.rsa \
   && python3 manage.py docgen circuit \
   && rm public-key.rsa
