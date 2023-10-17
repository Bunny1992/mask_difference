FROM python
ADD . /mask_difference
WORKDIR /mask_difference
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ENTRYPOINT ["python", "mask_difference.py"]