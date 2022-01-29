from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Customer, Profession, DataSheet, Document
from .serializers import CustomerSerializer, ProfessionSerializer, DataSheetSerializer, DocumentSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly, DjangoModelPermissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


# create four class CustomerViewSet, ProfessionViewSet, DataSheetViewSet, DocumentViewSet
class CustomerViewSet(viewsets.ModelViewSet):
    # queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('name',)
    search_fields = ('name', 'address', 'data_sheet__description')
    # search_fields = ('^name',) # fach ladir = katgolo 3tii la meme lhaja li brittha
    ordering_fields = ('id', 'name')
    ordering = ('-id',)  # hadi kat5dm par defaut
    lookup_field = 'doc_num'  # hadi kat5lik dir searching hi 3la l column li briti
    authentication_classes = [TokenAuthentication]

    # had function mo3rafa 3and django ou tlanca bo7dha bach dirna filter  Customer
    def get_queryset(self):
        # import pdb; pdb.set_trace()
        # had query_params katjiblk chno value d key like [{'active': 'True'}] rat3Tik self.request.query_params['active'] = 'True'
        address = self.request.query_params.get('address', None)
        print('address = ', address)
        if self.request.query_params.get('active') == 'False':
            status = False
        else:
            status = True
        if address:
            customers = Customer.objects.filter(address__icontains=address, active=status)
        else:
            customers = Customer.objects.filter(active=status)

        print('address = ' + str(address) + ' status = ' + str(status))
        return customers

    """def list(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        customers = self.get_queryset()
        serializer = CustomerSerializer(customers, many=True)
        print('\n', '-------------- list --------------', '\n')
        return Response(serializer.data)"""

    # had function t9ad dirha ila briti t affichi msg f7ala mkanch dak id li brit
    def retrieve(self, request, *args, **kwargs):
        customer = self.get_object()
        serializer = CustomerSerializer(customer)
        print('\n', '---------- retrieve ----------', '\n')
        return Response(serializer.data)
        # return HttpResponseNotAllowed('not - allowed')

    # creation d row f database --> PUT
    """def create(self, request, *args, **kwargs):
        data = request.data
        customer = Customer.objects.create(name=data['name'], address=data['address'], data_sheet_id=data['data_sheet'])

        profession = Profession.objects.get(id=data['profession'])
        customer.professions.add(profession)
        customer.save()

        serializer = CustomerSerializer(customer)
        print('\n', '--------------- create ----------------', '\n')
        return Response(serializer.data)"""

    # bach dir l update 3la row li briti li 3ndk f database --> wa9ila POST
    def update(self, request, *args, **kwargs):

        customer = self.get_object()
        data = request.data
        customer.name = data['name']
        customer.address = data['address']
        customer.data_sheet_id = data['data_sheet']
        profession = Profession.objects.get(id=data['profession'])

        for p in customer.professions.all():
            customer.professions.remove(p)
        customer.professions.add(profession)
        customer.save()

        serializer = CustomerSerializer(customer)
        print('\n', '--------------- update ----------------', '\n')
        return Response(serializer.data)

    # had function bach tbdl line w7d f database dyalk  --> PATCH
    def partial_update(self, request, *args, **kwargs):

        customer = self.get_object()
        customer.name = request.data.get('name', customer.name)
        customer.address = request.data.get('address', customer.address)
        customer.data_sheet_id = request.data.get('data_sheet', customer.data_sheet_id)
        customer.save()

        serializer = CustomerSerializer(customer)
        print('\n', '--------------- partial_update ----------------', '\n')
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):

        customer = self.get_object()
        customer.delete()
        print('\n', '--------------- destroy ----------------', '\n')
        return Response('Object removed')

    # had fucntion katsm7 tktb smit focntion f postman ou tzid id like customers/deactivate/4/
    @action(detail=True)
    def deactivate(self, request, **kwargs):
        table=["get-name"]
        customer = self.get_object()
        customer.active = False

        customer.save()
        serializer = CustomerSerializer(customer)
        print('\n', '--------------- deactivate ----------------', '\n')
        return Response(serializer.data)

    # ou hadi makatsm7ch tzid detail like tzid ina id briti specifik
    @action(detail=False)
    def deactivate_all(self, request, **kwargs):
        customers = self.get_queryset()
        print('customers = ', customers)
        customers.update(active=False)
        print('\n', 'customers.update(active=False) = ', customers.update(active=False))

        serializer = CustomerSerializer(customers, many=True)
        print('--------------- deactivate_all ----------------', '\n')
        print('-------------------------------', '\n')
        return Response(serializer.data)

    # ou hadi makatsm7ch tzid detail like tzid ina id briti specifik
    @action(detail=False)
    def activate_all(self, request, **kwargs):
        customers = self.get_queryset()
        customers.update(active=True)

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def change_status(self, request, **kwargs):

        status = True if request.data['active'] == 'True' else False
        customers = self.get_queryset()
        customers.update(active=status)

        serializer = CustomerSerializer(customers, many=True)
        print('\n', '--------------- change_status ----------------', '\n')
        return Response(serializer.data)


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    permission_classes = [IsAdminUser, ]  # hadi katsm7 l admin ra2isis houwa li st3ml l api


class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer
    permission_classes = [AllowAny, ]  # had any allow katsm7lk ta5d data wa5a matsift l code


# class DocumentViewSet
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    authentication_classes = [TokenAuthentication]
    # DjangoModelPermissions --> hadi kat3tik l7a9 bach t dir add ou delete oula update
    permission_classes = [IsAuthenticatedOrReadOnly, DjangoModelPermissions]
