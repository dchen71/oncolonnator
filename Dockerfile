FROM python:3.7.8-slim-buster

# Install necessary packages
RUN pip install pytest==5.4.3
RUN pip install pyvcf==0.6.8
RUN pip install requests==2.24.0
RUN pip install argparse==1.4.0
RUN pip install pandas==1.0.5

# Move scripts and example files
RUN mkdir /usr/scripts
COPY oncolonnator.py /usr/scripts
RUN chmod o+x /usr/scripts/oncolonnator.py
RUN mkdir /usr/scripts/input
RUN mkdir /usr/scripts/output
COPY input/example_input.vcf /usr/scripts/input
RUN chmod o+r /usr/scripts/input/example_input.vcf

# Run python entrypoint to pass in parameters
ENTRYPOINT ["python", "/usr/scripts/oncolonnator.py"]
