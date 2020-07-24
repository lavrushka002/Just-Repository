import pandas
import chardet

from sqlalchemy import create_engine
from django.conf import settings
from django.db.models import Avg, Count, Min, Sum
from rest_framework.response import Response
from rest_framework import status, generics
from deals.serializers import *
from deals.models import *

class DealsUploadView(generics.CreateAPIView):
	serializer_class = DataSerializer

	def generate_result_response(self):
		#5 customers who spent more money
		temp_result = Deal.objects.values('customer').annotate(Sum('total')).order_by('-total__sum')[:5]
		#load in db
		for i in temp_result:
			ResultResponse.objects.create(
				username = i['customer'],
				spent_money = i['total__sum']
			)
		#update db to add purchased gems
		for i in ResultResponse.objects.all():
			for j in Deal.objects.order_by('item').values('item', 'customer').distinct().filter(customer = i.username):
				ResultResponse.objects.filter(username = i.username).update(gems = ResultResponse.objects.get(username = i.username).gems + j['item'] + ': ')

	def csv_converter(self, path):
		with open(path, 'rb') as f:
			file_encode = chardet.detect(f.read())
			data = pandas.read_csv(
				filepath_or_buffer = path,
				encoding=file_encode['encoding'],
				sep=','
			)
		return data

	def post(self, request):
		file_serializer = DataSerializer(data=request.data)
		#delete all information from db from previous request
		ResultResponse.objects.all().delete()
		Deal.objects.all().delete()
		#save file path to db and generate result if file is valid, otherwise raise "exeption"
		if file_serializer.is_valid():
			file_serializer.save()
			engine = create_engine("postgresql://postgres:postgres@db/postgres")

			data = self.csv_converter(path = settings.MEDIA_URL + str(Data.objects.all().order_by('-id')[0]))
			data.to_sql(
				con = engine,
				name = Deal._meta.db_table,
				index = False,
				if_exists = 'append'
			)
#			data.to_sql(
#				name = Deal._meta.db_table,
#				con = sqlite3.connect('db.sqlite3'),
#				if_exists = 'append', index = False
#			)
			self.generate_result_response()

			return Response({'OK - файл был обработан без ошибок.'}, status=status.HTTP_201_CREATED)
		else:
			return Response({'В процессе обработки файла произошла ошибка.'}, status=status.HTTP_400_BAD_REQUEST)

class ResultResponseView(generics.ListAPIView):
	serializer_class = ResultSerializer
	queryset = ResultResponse.objects.all()