from django.db import models

# Create your models here.
class Endpoints(models.Model):
  '''
  The Endpoint object represents ML API endpoint.
  Attributes:
    name: The name of the endpoint, it will be used in API URL,
    owner: The string with owner name,
    created_at: The date when endpoint was created.
  '''
  name =  models.CharField(max_length=150)
  owner = models.CharField(max_length=120)
  created_at = models.DateTimeField(auto_now_add=True)

class MLAlgorithm(models.Model):
  '''
  The MLAlgorithm represent the ML algorithm object.

  Attributes:
    name: The name of the algorithm.
    code: The code of the algorithm.
    version: The version of the algorithm similar to software versioning.
    owner: The name of the owner.
    created_at: The date when MLAlgorithm was added.
    parent_endpoint: The reference to the Endpoint.
  '''
  name = models.CharField(max_length=128)
  code = models.CharField(max_length=6000)
  version = models.CharField(max_length=128)
  owner = models.CharField(max_length=128)
  created_at = models.DateTimeField(auto_now_add=True)
  parent_endpoint = models.ForeignKey(Endpoints,on_delete=models.CASCADE,related_name='algorithms')

class MLAlgorithmStatus(models.Model):
  '''
  The MLAlgorithmStatus represent status of the MLAlgorithm which can change during the time.
  Attributes:
    status: The status of algorithm in the endpoint. Can be: testing, staging, production, ab_testing.
    active: The boolean flag which point to currently active status.
    created_by: The name of creator.
    created_at: The date of status creation.
    parent_mlalgorithm: The reference to corresponding MLAlgorithm.
  '''
  OPTIONS = [('Testing','testing'), ('Staging','staging'), ('Production','production'), ('AB_Test','ab_testing')]
  status = models.CharField(max_length=50,choices=OPTIONS,default='Testing')
  active = models.BooleanField(default=False)
  created_by = models.CharField(max_length=128)
  created_at = models.DateTimeField(auto_now_add=True)
  parent_mlalgorithm = models.ForeignKey(MLAlgorithm,on_delete=models.CASCADE,related_name='status')

class MLRequest(models.Model):
  '''
  The MLRequest will keep information about all requests to ML algorithms.

  Attributes:
    input_data: The input data as text.
    full_response: The response of the ML algorithm.
    response: The response of the ML algorithm as text.
    feedback: The feedback about the models response.
    created_at: The date when request was created.
    parent_mlalgorithm: The reference to MLAlgorithm used to compute response.
  '''
  input_data = models.CharField(max_length=10000)
  full_response = models.CharField(max_length=10000)
  response = models.CharField(max_length=10000)
  feedback = models.CharField(max_length=10000)
  parent_mlalgorithm = models.ForeignKey(MLAlgorithm,related_name='request',on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)